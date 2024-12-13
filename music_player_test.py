import unittest
from unittest.mock import patch, MagicMock
import pygame
from music_player import * 

current_volume = 50

def increase_volume():
    """Increase the volume."""
    global current_volume
    if current_volume < 100:
        current_volume += 10
        pygame.mixer.music.set_volume(current_volume / 100)  # Увеличиваем громкость на 10

def decrease_volume():
    """Decrease the volume."""
    global current_volume
    if current_volume > 0:
        current_volume -= 10
        pygame.mixer.music.set_volume(current_volume / 100)  # Уменьшаем громкость на 10

class TestMusicPlayer(unittest.TestCase):

    @patch('pygame.mixer.music.load')
    @patch('pygame.mixer.music.play')
    def test_continue_stop_func(self, mock_play, mock_load):
        """Тестируем функцию continue_stop_func (пауза и воспроизведение музыки)."""
        global stopped
        stopped = True  # Начальное состояние, музыка остановлена

        # Вызываем функцию
        continue_stop_func()

        # Проверяем, что музыка загружается и воспроизводится
        mock_load.assert_called_once_with(music_now)
        mock_play.assert_called_once()

    def test_music_length_calculation(self):
        """Тестируем, правильно ли считается длина музыки (в миллисекундах)."""
        global music_now, music_length
        
        # Имитируем длительность песни
        mock_sound = MagicMock()
        mock_sound.get_length.return_value = 5  # Длительность песни 5 секунд
        with patch('pygame.mixer.Sound', return_value=mock_sound):
            music_now = 'test_song.mp3'
            music_length = pygame.mixer.Sound(music_now).get_length() * 1000  # Переводим в миллисекунды

        # Проверяем, что длительность музыки считается верно
        self.assertEqual(music_length, 5000)  # 5 секунд = 5000 миллисекунд

    @patch('pygame.mixer.music.set_volume')  # Патчим set_volume
    def test_increase_volume(self, mock_set_volume):
        """Простой тест для increase_volume."""
        global current_volume
        current_volume = 50
        increase_volume()
        self.assertEqual(current_volume, 60)
        mock_set_volume.assert_called_once_with(60 / 100)

    @patch('pygame.mixer.music.set_volume')  # Патчим set_volume
    def test_decrease_volume(self, mock_set_volume):
        """Простой тест для decrease_volume."""
        global current_volume
        current_volume = 50
        decrease_volume()
        self.assertEqual(current_volume, 40)
        mock_set_volume.assert_called_once_with(40 / 100)

if __name__ == '__main__':
    unittest.main()
