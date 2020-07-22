import parameters as p
from images import *
from sounds import *
from insects import *
from object import *


class Game:
    def __init__(self):
        pygame.display.set_caption('Weekdays Storekeeper!')
        pygame.display.set_icon(icon)

        pygame.mixer_music.load('sound_effects/background.wav')
        pygame.mixer_music.set_volume(0.1)
        pygame.mixer.music.play(-1)

        self.make_jump = False
        self.moving_left = False
        self.moving_right = False
        self.first_spawn = False
        self.first_change_color = False
        self.second_change_color = False
        self.third_change_color = False

        self.jump_counter = 30
        self.cooldown = 100
        self.kill_cooldown = 0
        self.cooldown_second = 120
        self.spawn_insects_cooldown = 0
        self.spawn_insect_cooldown = 0

        self.all_creates = []
        self.all_insect = []

        self.first_create = Crate(500, box, 0)
        self.second_create = Crate(500, soap, 150)
        self.third_create = Crate(500, box, 550)
        self.first_insect_rat = Insects(rat, 30, 460)
        self.second_insect_roach = Insects(cockroach, 180, 440)
        self.third_insect_roach = Insects(cockroach, 570, 440)

        self.second_insect_rat = Insects(rat, 180, 460)
        self.third_insect_rat = Insects(rat, 570, 440)

        self.first_create_hp = 105
        self.second_create_hp = 105
        self.third_create_hp = 105
        self.money = 3000
        self.health = 3
        self.score = 0
        self.max_score = 0
        self.poison = 3

        self.cloud = self.open_random_objects()

    def start_game(self):
        game = True

        self.all_respawn()

        while game:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()

            if self.cooldown != 0:
                self.cooldown -= 1
            elif self.cooldown == 0:
                self.first_spawn = True

            keys = pygame.key.get_pressed()

            if keys[pygame.K_SPACE]:
                self.make_jump = True

            if self.make_jump:
                self.jump()

            if keys[pygame.K_a]:
                self.moving_left = True

            if self.moving_left:
                self.move_to_left()

            if keys[pygame.K_d]:
                self.moving_right = True

            if self.moving_right:
                self.move_to_right()

            if self.kill_cooldown == 0:
                if keys[pygame.K_x]:
                    if self.poison > 0:
                        if self.first_insect_rat.location_x <= p.usr_x <= self.first_insect_rat.location_x + 60:
                            if self.first_spawn:
                                self.del_first_rat()
                                self.poison -= 0.5
                                self.score += 0.5

                        if self.second_insect_roach.location_x <= p.usr_x <= self.second_insect_roach.location_x + 62:
                            if self.first_spawn:
                                self.del_second_roach()
                                self.poison -= 0.5
                                self.score += 0.5
                                self.kill_cooldown = 20

                        if self.second_insect_roach not in self.all_insect:
                            if self.second_insect_rat.location_x <= p.usr_x <= self.second_insect_rat.location_x + 60:
                                if self.first_spawn:
                                    self.del_second_rat()
                                    self.poison -= 0.5
                                    self.score += 0.5

                        if self.third_insect_roach.location_x <= p.usr_x <= self.third_insect_roach.location_x + 62:
                            if self.first_spawn:
                                self.del_third_roach()
                                self.poison -= 0.5
                                self.score += 0.5
                                self.kill_cooldown = 20

                        if self.third_insect_roach not in self.all_insect:
                            if self.third_insect_rat.location_x <= p.usr_x <= self.third_insect_rat.location_x + 60:
                                if self.first_spawn:
                                    self.del_third_rat()
                                    self.poison -= 0.5
                                    self.score += 0.5
            else:
                self.kill_cooldown -= 1

            if keys[pygame.K_ESCAPE]:
                self.pause()

            if not self.spawn_insect_cooldown:
                if keys[pygame.K_e]:
                    if p.sale_x <= p.usr_x <= p.sale_x + p.sale_x + 100:
                        if self.first_create not in self.all_creates:
                            self.all_creates.append(self.first_create)
                            self.money += 500
                            self.first_create_hp = 100
                            self.all_insect.append(self.first_insect_rat)
                            self.spawn_insect_cooldown = 30
                        if self.second_create not in self.all_creates:
                            self.all_creates.append(self.second_create)
                            self.money += 500
                            self.second_create = 100
                            self.all_insect.append(self.second_insect_roach)
                            self.spawn_insect_cooldown = 30
                        if self.third_create not in self.all_creates:
                            self.all_creates.append(self.third_create)
                            self.money += 500
                            self.third_create = 100
                            self.all_insect.append(self.third_insect_roach)
                            self.spawn_insect_cooldown = 30
            else:
                self.spawn_insect_cooldown -= 1

            if keys[pygame.K_y]:
                if self.money >= 500:
                    self.poison += 1
                    self.money -= 500

            if self.first_insect_rat in self.all_insect:
                self.main_damage(1)

            if self.second_insect_roach in self.all_insect or self.second_insect_rat in self.all_insect:
                self.main_damage(2)

            if self.third_insect_roach in self.all_insect or self.third_insect_rat in self.all_insect:
                self.main_damage(3)

            if self.first_create_hp <= 0:
                self.del_first_rat()
                self.del_first_create()

            if self.second_create_hp <= 0:
                if self.second_insect_rat in self.all_insect:
                    self.del_second_rat()
                    self.del_second_create()
                elif self.second_insect_roach in self.all_insect:
                    self.del_second_roach()
                    self.del_second_create()

            if self.third_create_hp <= 0:
                if self.third_insect_rat in self.all_insect:
                    self.del_third_rat()
                    self.del_third_create()
                elif self.third_insect_roach in self.all_insect:
                    self.del_third_roach()
                    self.del_third_create()

            # Логика перемещения крысы
            if self.first_insect_rat in self.all_insect and self.first_create in self.all_creates:
                if self.second_insect_roach not in self.all_insect:
                    if self.second_create in self.all_creates:
                        if self.second_insect_rat not in self.all_creates:
                            self.del_first_rat()
                            self.all_insect.append(self.second_insect_rat)

            if self.second_insect_rat not in self.all_insect:
                if self.third_create in self.all_creates and self.third_insect_roach not in self.all_insect:
                    if self.third_insect_rat not in self.all_insect and self.first_insect_rat not in self.all_insect:
                        self.del_second_rat()
                        self.all_insect.append(self.third_insect_rat)

            if self.second_create not in self.all_creates and self.second_insect_roach not in self.all_insect \
                    and self.second_insect_rat not in self.all_insect:
                if self.third_create not in self.all_creates and self.third_insect_rat not in self.all_insect:
                    if self.first_create in self.all_creates:
                        self.del_third_rat()
                        self.all_insect.append(self.first_insect_rat)

            if self.second_create in self.all_insect and self.second_insect_roach not in self.all_insect:
                if self.third_create not in self.all_insect:
                    self.all_insect.append(self.second_insect_rat)

            if self.first_insect_rat not in self.all_insect and self.second_insect_rat not in self.all_insect:
                if self.first_create not in self.all_creates and self.second_create not in self.all_creates:
                    self.del_third_rat()

            if self.first_insect_rat not in self.all_insect and self.second_insect_rat not in self.all_insect:
                if self.first_create not in self.all_creates and self.second_create in self.all_creates:
                    self.del_third_rat()

            if self.first_insect_rat not in self.all_insect and self.second_insect_rat not in self.all_insect:
                if self.first_create in self.all_creates and self.second_create not in self.all_creates:
                    self.del_third_rat()

            if self.first_insect_rat not in self.all_insect and self.second_insect_rat not in self.all_insect:
                if self.first_create in self.all_creates and self.second_create in self.all_creates:
                    self.del_third_rat()

            if not self.spawn_insect_cooldown:
                if self.first_create not in self.all_creates and self.second_create not in self.all_creates:
                    if self.third_create not in self.all_creates:
                        self.health -= 1
                        self.all_respawn()
                        self.spawn_insect_cooldown = 35
                        if self.health <= 0:
                            pygame.mixer.Sound.play(loss_sound)
                            game = False
                        else:
                            pygame.mixer.Sound.play(fall_sound)
            else:
                self.spawn_insect_cooldown -= 1

            # Логика респавна ящиков и насекомых
            if self.first_create in self.all_creates and self.first_insect_rat not in self.all_insect:
                if self.second_create in self.all_creates and self.second_insect_roach not in self.all_insect \
                        and self.second_insect_rat not in self.all_insect:
                    if self.third_create in self.all_creates and self.third_insect_roach not in self.all_insect \
                            and self.third_insect_rat not in self.all_insect:
                        self.all_respawn()
                        self.money += 1500

            if self.first_create in self.all_creates and self.second_create in self.all_creates and self.third_create \
                    not in self.all_creates:
                if self.first_insect_rat not in self.all_insect and self.second_insect_roach not in self.all_insect \
                        and self.third_insect_roach not in self.all_insect:
                    if self.second_insect_rat not in self.all_insect and self.third_insect_rat not in self.all_insect:
                        if self.cooldown_second == 0:
                            self.all_insect.append(self.first_insect_rat)
                            self.all_insect.append(self.second_insect_roach)
                            self.money += 1000
                            self.cooldown_second = 120
                        else:
                            self.cooldown_second -= 1

            if self.second_create in self.all_creates and self.third_create in self.all_creates and self.first_create not in self.all_insect:
                if self.second_insect_roach not in self.all_insect and self.third_insect_roach not in self.all_insect:
                    if self.second_insect_rat not in self.all_insect and self.third_insect_rat not in self.all_insect:
                        if self.cooldown_second == 0:
                            self.all_insect.append(self.second_insect_roach)
                            self.all_insect.append(self.third_insect_roach)
                            self.money += 1000
                            self.cooldown_second = 120
                        else:
                            self.cooldown_second -= 1

            if self.first_create in self.all_creates and self.third_create in self.all_creates and self.second_create not in self.all_insect:
                if self.first_insect_rat not in self.all_insect and self.third_insect_roach not in self.all_insect:
                    if self.third_insect_rat not in self.all_insect:
                        if self.cooldown_second == 0:
                            self.all_insect.append(self.first_insect_rat)
                            self.all_insect.append(self.third_insect_roach)
                            self.money += 1000
                            self.cooldown_second = 120
                        else:
                            self.cooldown_second -= 1

            p.display.blit(land, (0, 0))
            self.draw_storekeeper()
            self.draw_saleman()
            self.print_text('Scores: ' + str(int(self.score)), 20, 60)
            self.print_text(str(self.money), font_color=(251, 10, 250), x=90, y=110, font_size=30)
            self.print_text(str(int(self.poison)), font_color=(0, 254, 64), x=100, y=195, font_size=30)
            self.print_text('Y - buy poison', font_size=15, x=690, y=485)
            self.print_text('E - respawn create(s)', font_size=13, x=663, y=470)
            if self.first_spawn:
                self.draw_crates(self.all_creates)
                self.draw_insects(self.all_insect)
                self.draw_hp()
                self.show_hearts()
                self.show_money()
                self.show_poison()
                self.move_objects(self.cloud)

            pygame.display.update()
            p.clock.tick(60)

    def del_first_rat(self):
        for i in self.all_insect:
            if i == self.first_insect_rat:
                self.all_insect.remove(i)

    def del_second_roach(self):
        for i in self.all_insect:
            if i == self.second_insect_roach:
                self.all_insect.remove(i)

    def del_second_rat(self):
        for i in self.all_insect:
            if i == self.second_insect_rat:
                self.all_insect.remove(i)

    def del_third_rat(self):
        for i in self.all_insect:
            if i == self.third_insect_rat:
                self.all_insect.remove(i)

    def del_third_roach(self):
        for i in self.all_insect:
            if i == self.third_insect_roach:
                self.all_insect.remove(i)

    def del_first_create(self):
        for i in self.all_creates:
            if i == self.first_create:
                self.all_creates.remove(i)

    def del_second_create(self):
        for i in self.all_creates:
            if i == self.second_create:
                self.all_creates.remove(i)

    def del_third_create(self):
        for i in self.all_creates:
            if i == self.third_create:
                self.all_creates.remove(i)

    def all_respawn(self):
        self.all_creates.append(self.first_create)
        self.all_insect.append(self.first_insect_rat)
        self.all_creates.append(self.second_create)
        self.all_insect.append(self.second_insect_roach)
        self.all_creates.append(self.third_create)
        self.all_insect.append(self.third_insect_roach)
        self.first_create_hp = 100
        self.second_create_hp = 100
        self.third_create_hp = 100

    def draw_storekeeper(self):
        p.display.blit(gg, (p.usr_x, p.usr_y))

    def draw_saleman(self):
        p.display.blit(saleman, (p.sale_x, p.sale_y))

    def draw_crates(self, creates):
        for create in creates:
            create.draw()

    def draw_insects(self, insects):
        for insect in insects:
            insect.draw()

    def show_hearts(self):
        show = 0
        x = 20
        while show != self.health:
            display.blit(heart, (x, 20))
            x += 40
            show += 1

    def show_poison(self):
        display.blit(poison, (15, 175))

    def show_money(self):
        display.blit(money, (20, 100))

    def pause(self):
        paused = True
        while paused:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()

            self.print_text('Paused. Press enter to continue', 160, 300)

            keys = pygame.key.get_pressed()
            if keys[pygame.K_RETURN]:
                paused = False

            pygame.display.update()
            p.clock.tick(15)

    def draw_hp(self):
        self.print_text((str(int(self.first_create_hp))), 40, 420, font_color=(253, 0, 15),
                        font_type='fonts/storekeeper.ttf', font_size=35)

        self.print_text(str(int(self.second_create_hp)), 190, 410, font_color=(253, 0, 15),
                        font_type='fonts/storekeeper.ttf', font_size=35)

        self.print_text(str(int(self.third_create_hp)), 580, 400, font_color=(253, 0, 15),
                        font_type='fonts/storekeeper.ttf', font_size=35)

    def main_damage(self, create_num):
        if create_num == 1:
            if self.first_create_hp >= 0:
                self.first_create_hp -= 0.08
        elif create_num == 2:
            if self.second_create_hp >= 0:
                self.second_create_hp -= 0.05
        elif create_num == 3:
            if self.third_create_hp >= 0:
                self.third_create_hp -= 0.05

    def jump(self):
        if self.jump_counter >= -30:
            if self.jump_counter == -10:
                pygame.mixer.Sound.play(fall_sound)

            p.usr_y -= self.jump_counter / 2
            self.jump_counter -= 1
        else:
            self.jump_counter = 30
            self.make_jump = False

    def move_to_left(self):
        if self.moving_left:
            if p.usr_x - 5 < 0:
                p.usr_x = 0
            else:
                p.usr_x = p.usr_x - 5
            self.moving_left = False

    def move_to_right(self):
        if self.moving_right:
            if p.usr_x + 5 > 705:
                p.usr_x = 710
            else:
                p.usr_x = p.usr_x + 5
            self.moving_right = False

    def print_text(self, message, x, y, font_color=(0, 0, 0), font_type='fonts/storekeeper.ttf', font_size=30):
        self.font_type = pygame.font.Font(font_type, font_size)
        self.text = self.font_type.render(message, True, font_color)
        p.display.blit(self.text, (x, y))

    def open_random_objects(self):
        choice = random.randrange(0, 2)
        img_of_cloud = cloud_img[choice]

        cloud = Object(p.display_width, 80, 70, img_of_cloud, 2)

        return cloud

    @staticmethod
    def move_objects(cloud):
        check = cloud.move()
        if not check:
            choice = random.randrange(0, 2)
            img_of_cloud = cloud_img[choice]
            cloud.return_self(p.display_width, random.randrange(10, 150), cloud.width, img_of_cloud)


a = Game()
a.start_game()
quit()
