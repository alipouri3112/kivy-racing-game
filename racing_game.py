from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.graphics import Rectangle, Color, Ellipse
from kivy.core.window import Window
from kivy.clock import Clock
from kivy.properties import NumericProperty
import random

class Car(Widget):
    def __init__(self, **kwargs):
        super(Car, self).__init__(**kwargs)
        self.size = (50, 80)
        with self.canvas:
            Color(0.2, 0.6, 1)
            self.rect = Rectangle(pos=self.pos, size=self.size)
        self.bind(pos=self.update_rect)

    def update_rect(self, *args):
        self.rect.pos = self.pos

    def move_left(self):
        if self.x > 50:
            self.x -= 20

    def move_right(self):
        if self.right < Window.width - 50:
            self.x += 20

class EnemyCar(Widget):
    def __init__(self, **kwargs):
        super(EnemyCar, self).__init__(**kwargs)
        self.size = (50, 80)
        colors = [(1, 0, 0), (1, 0.5, 0), (0.8, 0, 0.8), (1, 1, 0)]
        color = random.choice(colors)
        with self.canvas:
            Color(*color)
            self.rect = Rectangle(pos=self.pos, size=self.size)
        self.bind(pos=self.update_rect)

    def update_rect(self, *args):
        self.rect.pos = self.pos

class Road(Widget):
    def __init__(self, **kwargs):
        super(Road, self).__init__(**kwargs)
        with self.canvas:
            Color(0.3, 0.3, 0.3)
            Rectangle(pos=(50, 0), size=(Window.width - 100, Window.height))
            Color(1, 1, 1)
            for i in range(0, int(Window.height) + 100, 100):
                Rectangle(pos=(Window.width / 2 - 5, i), size=(10, 50))

class TouchButton(Widget):
    def __init__(self, text, callback, **kwargs):
        super(TouchButton, self).__init__(**kwargs)
        self.callback = callback
        self.text = text
        self.size = (80, 80)
        with self.canvas:
            Color(0.2, 0.2, 0.2, 0.7)
            self.bg = Ellipse(pos=self.pos, size=self.size)
        self.label = Label(text=text, center=self.center, font_size='30sp', bold=True)
        self.add_widget(self.label)
        self.bind(pos=self.update_graphics, size=self.update_graphics)

    def update_graphics(self, *args):
        self.bg.pos = self.pos
        self.bg.size = self.size
        self.label.center = self.center

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            self.callback()
            return True
        return super(TouchButton, self).on_touch_down(touch)

class RacingGame(Widget):
    score = NumericProperty(0)
    game_over = False
    
    def __init__(self, **kwargs):
        super(RacingGame, self).__init__(**kwargs)
        
        # جاده
        self.road = Road()
        self.add_widget(self.road)
        
        # ماشین بازیکن
        self.player = Car()
        self.player.pos = (Window.width / 2 - 25, 80)
        self.add_widget(self.player)
        
        # ماشین‌های دشمن
        self.enemies = []
        
        # امتیاز
        self.score_label = Label(
            text='Score: 0',
            pos=(10, Window.height - 50),
            size_hint=(None, None),
            font_size='20sp'
        )
        self.add_widget(self.score_label)
        
        # دکمه‌های لمسی برای موبایل
        self.left_btn = TouchButton('<', self.player.move_left)
        self.left_btn.pos = (20, 20)
        self.add_widget(self.left_btn)
        
        self.right_btn = TouchButton('>', self.player.move_right)
        self.right_btn.pos = (Window.width - 100, 20)
        self.add_widget(self.right_btn)
        
        # کیبورد برای کامپیوتر
        try:
            self._keyboard = Window.request_keyboard(self._keyboard_closed, self)
            if self._keyboard:
                self._keyboard.bind(on_key_down=self._on_keyboard_down)
        except:
            pass  # اگه کیبورد در دسترس نبود
        
        # شروع بازی
        Clock.schedule_interval(self.update, 1.0 / 60.0)
        Clock.schedule_interval(self.spawn_enemy, 1.5)
        
    def _keyboard_closed(self):
        if self._keyboard:
            self._keyboard.unbind(on_key_down=self._on_keyboard_down)
            self._keyboard = None

    def _on_keyboard_down(self, keyboard, keycode, text, modifiers):
        if not self.game_over:
            if keycode[1] in ['left', 'a']:
                self.player.move_left()
            elif keycode[1] in ['right', 'd']:
                self.player.move_right()
        return True

    def spawn_enemy(self, dt):
        if not self.game_over:
            enemy = EnemyCar()
            # موقعیت‌های ممکن در جاده
            lane_width = (Window.width - 100) / 4
            lanes = [50 + lane_width * i + lane_width/2 - 25 for i in range(4)]
            enemy.x = random.choice(lanes)
            enemy.y = Window.height
            self.enemies.append(enemy)
            self.add_widget(enemy)

    def update(self, dt):
        if self.game_over:
            return
            
        # سرعت افزایش می‌یابد
        speed = 5 + (self.score / 100)
        
        # حرکت ماشین‌های دشمن
        for enemy in self.enemies[:]:
            enemy.y -= speed
            
            # حذف ماشین‌های خارج شده
            if enemy.y < -100:
                self.remove_widget(enemy)
                self.enemies.remove(enemy)
                self.score += 10
                self.score_label.text = f'Score: {self.score}'
            
            # بررسی برخورد
            elif self.check_collision(self.player, enemy):
                self.end_game()
                break

    def check_collision(self, car1, car2):
        # بررسی دقیق‌تر برخورد با حاشیه ایمنی
        margin = 10
        return (car1.x + margin < car2.x + car2.width - margin and
                car1.x + car1.width - margin > car2.x + margin and
                car1.y + margin < car2.y + car2.height - margin and
                car1.y + car1.height - margin > car2.y + margin)

    def end_game(self):
        self.game_over = True
        
        # توقف تمام ماشین‌ها
        Clock.unschedule(self.update)
        Clock.unschedule(self.spawn_enemy)
        
        # پیام پایان بازی
        game_over_label = Label(
            text=f'Game Over!\nFinal Score: {self.score}',
            center=(Window.width / 2, Window.height / 2 + 50),
            size_hint=(None, None),
            font_size='30sp',
            halign='center'
        )
        self.add_widget(game_over_label)
        
        # دکمه شروع مجدد
        restart_btn = Button(
            text='Restart',
            center=(Window.width / 2, Window.height / 2 - 50),
            size_hint=(None, None),
            size=(150, 50)
        )
        restart_btn.bind(on_press=self.restart_game)
        self.add_widget(restart_btn)

    def restart_game(self, instance):
        # پاک کردن کیبورد
        if hasattr(self, '_keyboard') and self._keyboard:
            self._keyboard_closed()
        
        # پاک کردن بازی فعلی
        self.clear_widgets()
        
        # ریست کردن متغیرها
        self.score = 0
        self.game_over = False
        self.enemies = []
        
        # ساخت مجدد بازی
        # جاده
        self.road = Road()
        self.add_widget(self.road)
        
        # ماشین بازیکن
        self.player = Car()
        self.player.pos = (Window.width / 2 - 25, 80)
        self.add_widget(self.player)
        
        # امتیاز
        self.score_label = Label(
            text='Score: 0',
            pos=(10, Window.height - 50),
            size_hint=(None, None),
            font_size='20sp'
        )
        self.add_widget(self.score_label)
        
        # دکمه‌های لمسی
        self.left_btn = TouchButton('<', self.player.move_left)
        self.left_btn.pos = (20, 20)
        self.add_widget(self.left_btn)
        
        self.right_btn = TouchButton('>', self.player.move_right)
        self.right_btn.pos = (Window.width - 100, 20)
        self.add_widget(self.right_btn)
        
        # کیبورد
        try:
            self._keyboard = Window.request_keyboard(self._keyboard_closed, self)
            if self._keyboard:
                self._keyboard.bind(on_key_down=self._on_keyboard_down)
        except:
            pass
        
        # شروع مجدد بازی
        Clock.schedule_interval(self.update, 1.0 / 60.0)
        Clock.schedule_interval(self.spawn_enemy, 1.5)

class RacingApp(App):
    def build(self):
        Window.clearcolor = (0.1, 0.1, 0.1, 1)
        return RacingGame()

if __name__ == '__main__':
    RacingApp().run()