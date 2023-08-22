import random
from thread_management import ThreadManager
from typing import List, Tuple
from gui_components import Scene, TextButton, MouseEventAdapter, Component, RoundButton, Surface, Label
from game_resource import image, constants, audio
from game_element import PlayerEffectCreatingInformation, player_factory, card_factory
from decorator import singleton
import pymsgbox

from .game import Game
from .delay import delay


class Pool:
    PLAYER: str = "player"
    CARD: str = "card"
    _pool: List[int]
    _type: str
    _cost: int

    def __init__(self, pool: List[int], type: str, cost: int) -> None:
        self._pool = pool
        self._type = type
        self._cost = cost

    def draw(self):
        if self.check_all_content_full_grown():
            return None
        if Game().get_user_point() > self._cost:
            Game().add_user_point(- self._cost)
            return (self._type, random.choice([content for content in self._pool if not self._check_content_full_grown(content)]))
        return None

    def get_all_pool_content(self):
        return [content for content in self._pool]

    def check_all_content_full_grown(self):
        return all(self._check_content_full_grown(content) for content in self._pool)

    def _check_content_full_grown(self, content: int):
        if self._type == Pool.PLAYER:
            player_creating_information = Game().get_player_creating_information(content)
            return player_creating_information.hp >= player_creating_information.max_hp and player_creating_information.shield >= player_creating_information.max_shield
        elif self._type == Pool.CARD:
            return content in Game().get_unlock_card_id_list()
        return True


@singleton
class GachaScene(Scene):
    _reserved_comp_list: List[Component]
    _page_list: List[Tuple[Component, Pool, Component]]
    _current_page: int

    def __init__(self) -> None:
        super().__init__(image.get_image(image.BG_MENU),
                         (constants.WINDOW_WIDTH, constants.WINDOW_HEIGHT))
        self._reserved_comp_list = []

        self._page_list = []
        self._current_page = None

        btn_spacing = 5

        left_btn = RoundButton(image.get_image(image.BTN_LEFT_UP),
                               image.get_image(image.BTN_LEFT_DOWN))
        left_btn.set_x(self.get_centerx() - left_btn.get_width() - 10)
        left_btn.set_y(self.get_height() - left_btn.get_height())
        left_btn.add_mouse_handler(MouseEventAdapter(
            mouse_click=lambda event: self._go_left_page()))
        right_btn = RoundButton(image.get_image(image.BTN_RIGHT_UP),
                                image.get_image(image.BTN_RIGHT_DOWN))
        right_btn.set_x(self.get_centerx() + 10)
        right_btn.set_y(self.get_height() - right_btn.get_height())
        right_btn.add_mouse_handler(MouseEventAdapter(
            mouse_click=lambda event: self._go_right_page()))
        self.add_component(left_btn)
        self.add_component(right_btn)
        self._reserved_comp_list.append(left_btn)
        self._reserved_comp_list.append(right_btn)

        def close_detail():
            self._turn_to_page(self._current_page)
        close_detail_btn = TextButton("返回")
        close_detail_btn.add_mouse_handler(
            MouseEventAdapter(mouse_click=lambda event: close_detail()))
        close_detail_btn.set_pos((self.get_width() - close_detail_btn.get_width(),
                                  self.get_height() - close_detail_btn.get_height()))

        def show_detail():
            self.clear_component()
            pool_detail = self._page_list[self._current_page][2]
            pool_detail.set_center((self.get_width()//2, self.get_height()//2))
            self.add_component(pool_detail)
            self.add_component(close_detail_btn)
        show_detail_btn = TextButton("獎池資訊")
        show_detail_btn.add_mouse_handler(
            MouseEventAdapter(mouse_click=lambda event: show_detail()))
        show_detail_btn.set_pos((self.get_width() - show_detail_btn.get_width() * 2 - btn_spacing,
                                 self.get_height() - show_detail_btn.get_height()))
        self.add_component(show_detail_btn)
        self._reserved_comp_list.append(show_detail_btn)

        back_btn = TextButton("返回")
        back_btn.add_mouse_handler(
            MouseEventAdapter(mouse_click=lambda event: Game().remove_scene(self)))
        back_btn.set_pos((self.get_width() - back_btn.get_width(),
                          self.get_height() - back_btn.get_height()))
        self.add_component(back_btn)
        self._reserved_comp_list.append(back_btn)

        draw_btn = TextButton("抽")
        draw_btn.add_mouse_handler(
            MouseEventAdapter(mouse_click=lambda event: self._draw()))
        draw_btn.set_center((self.get_width()//2,
                             self.get_height()//2))
        self.add_component(draw_btn)
        self._reserved_comp_list.append(draw_btn)

    def _draw(self):
        if self._page_list[self._current_page][1].check_all_content_full_grown():
            pymsgbox.alert("已經抽滿拉", "肝帝請受我一拜")
            return
        result = self._page_list[self._current_page][1].draw()
        if result == None:
            pymsgbox.alert("Pt不足", "再一單")
            return
        result_type = result[0]
        result_id = result[1]
        if result_type == Pool.PLAYER:
            if result_id in Game().get_unlock_player_id_list():
                player_creating_information = Game().get_player_creating_information(result_id)
                player_creating_information.hp = min(
                    player_creating_information.hp + 3, player_creating_information.max_hp)
                player_creating_information.shield = min(
                    player_creating_information.shield + 4, player_creating_information.max_shield)
                Game().set_player_creating_information(player_creating_information)
            else:
                Game().add_unlock_player_id(result_id)
            ThreadManager().run_func_as_new_thread(target=self._show_draw_player, args=[
                result_id, self._page_list[self._current_page][1].get_all_pool_content()])
        elif result_type == Pool.CARD:
            if result_id not in Game().get_unlock_card_id_list():
                Game().add_unlock_card_id(result_id)
            ThreadManager().run_func_as_new_thread(target=self._show_draw_card, args=[
                result_id, self._page_list[self._current_page][1].get_all_pool_content()])

    def _show_draw_player(self, player_id: int, pool_player_id_list: List[int]):
        self.clear_component()
        black_bg = Component(Surface((self.get_width(), self.get_height())))
        self.add_component(black_bg)

        temp_comp_list = []
        for _ in range(20):
            delay(100)
            comp = player_factory.get_player_fullbody_comp(
                random.choice(pool_player_id_list))
            comp.set_center((random.randint(0, self.get_width()),
                            random.randint(0, self.get_height())))
            self.add_component(comp)
            temp_comp_list.append(comp)

        for comp in temp_comp_list:
            self.remove_component(comp)
        delay(500)
        audio.get_sound(audio.EFFECT_DRAW_CARD).play()
        drawn_player = player_factory.get_player_fullbody_comp(player_id)
        drawn_player.set_center((self.get_width()//2, self.get_height()//2))
        self.add_component(drawn_player)
        delay(1000)
        self._turn_to_page(self._current_page)

    def _show_draw_card(self, card_id: int, pool_card_id_list: List[int]):
        self.clear_component()
        black_bg = Component(Surface((self.get_width(), self.get_height())))
        self.add_component(black_bg)

        temp_comp_list = []
        for _ in range(20):
            delay(100)
            comp = card_factory.get_card(random.choice(pool_card_id_list))
            comp.set_center((random.randint(0, self.get_width()),
                            random.randint(0, self.get_height())))
            self.add_component(comp)
            temp_comp_list.append(comp)

        for comp in temp_comp_list:
            self.remove_component(comp)
        delay(500)
        audio.get_sound(audio.EFFECT_DRAW_CARD).play()
        drawn_card = card_factory.get_card(card_id)
        drawn_card.set_center((self.get_width()//2, self.get_height()//2))
        self.add_component(drawn_card)
        delay(1000)
        self._turn_to_page(self._current_page)

    def start_showing(self):
        ThreadManager().run_func_as_new_thread(target=self._show_pool_thread_func)

    def _show_pool_thread_func(self):
        self.clear_component()
        self._page_list = [
            (Component(image.get_image(image.GACHA_POOL_BASEPLAYER)),
             Pool(
                 [player_id for player_id in player_factory.get_all_player_id()], Pool.PLAYER, 10),
             Component(image.get_image(image.GACHA_POOL_DETAIL_BASEPLAYER))),
        ]
        self._turn_to_page(0)

    def _go_left_page(self) -> None:
        if self._current_page > 0:
            self._turn_to_page(self._current_page - 1)

    def _go_right_page(self) -> None:
        if self._current_page < len(self._page_list) - 1:
            self._turn_to_page(self._current_page + 1)

    def _show_user_point(self):
        user_point_label = Label(
            f"Pt: {Game().get_user_point()}", constants.COLOR_WHITE)
        user_point_label_bg = Component(Surface(user_point_label.get_size()))
        self.add_component(user_point_label_bg)
        self.add_component(user_point_label)

    def _turn_to_page(self, page: int) -> None:
        self.clear_component()
        self._show_user_point()
        for comp in self._reserved_comp_list:
            self.add_component(comp)
        self._current_page = page
        self.add_component(self._page_list[self._current_page][0], 0)
