from dataclasses import dataclass


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""
    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float

    def get_message(self) -> str:
        """Вывод сообщения о тренировке."""
        return(f'Тип тренировки: {self.training_type}; '
               f'Длительность: {self.duration:.3f} ч.; '
               f'Дистанция: {self.distance:.3f} км; '
               f'Ср. скорость: {self.speed:.3f} км/ч; '
               f'Потрачено ккал: {self.calories:.3f}.'
               )


@dataclass
class Training:
    """Базовый класс тренировки."""
    LEN_STEP = 0.65
    M_IN_KM = 1000

    action: int
    duration: float
    weight: float

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        distance = self.action * self.LEN_STEP / self.M_IN_KM
        return distance

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        mean_speed = self.get_distance() / self.duration
        return mean_speed

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        raise NotImplementedError(
            f'Определите get_spent_calories в {self.__class__.__name__}'
        )

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(type(self).__name__,
                           self.duration,
                           self.get_distance(),
                           self.get_mean_speed(),
                           self.get_spent_calories()
                           )


class Running(Training):
    """Тренировка: бег."""
    COEFF_CALORIE_1 = 18
    COEFF_CALORIE_2 = 20
    H_IN_MIN = 60

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        spent_calories = ((self.COEFF_CALORIE_1 * super().get_mean_speed()
                          - self.COEFF_CALORIE_2) * self.weight
                          / self.M_IN_KM * self.duration * self.H_IN_MIN
                          )
        return spent_calories


@dataclass
class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    COEFF_CALORIE_1 = 0.035
    COEFF_CALORIE_2 = 0.029
    H_IN_MIN = 60

    height: float

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        spent_calories = ((self.COEFF_CALORIE_1 * self.weight
                          + (super().get_mean_speed()**2 // self.height)
                          * self.COEFF_CALORIE_2 * self.weight)
                          * self.duration * self.H_IN_MIN
                          )
        return spent_calories


@dataclass
class Swimming(Training):
    """Тренировка: плавание."""
    LEN_STEP = 1.38
    COEFF_CALORIE_1 = 1.1
    COEFF_CALORIE_2 = 2

    length_pool: float
    count_pool: float

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        distance = self.action * self.LEN_STEP / self.M_IN_KM
        return distance

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        mean_speed = (self.length_pool * self.count_pool
                      / self.M_IN_KM / self.duration
                      )
        return mean_speed

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        spent_calories = ((self.get_mean_speed() + self.COEFF_CALORIE_1)
                          * self.COEFF_CALORIE_2 * self.weight
                          )
        return spent_calories


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    workouts = {
        'RUN': Running,
        'WLK': SportsWalking,
        'SWM': Swimming,
    }
    try:
        if workout_type not in workouts:
            raise KeyError('Неизвестный тип тренировки')
    except KeyError:
        raise
    else:
        # определяем класс тренировки
        workout = workouts[workout_type]
        # создаем объект соотв. класса
        training: workout = workout(*data)
        return training


def main(training: Training) -> None:
    """Главная функция."""
    info = training.show_training_info()
    print(info.get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
