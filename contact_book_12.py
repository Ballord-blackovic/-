class Member:
    def __init__(self, surname=None, name=None, namb=None, bd=None, adrs=None, from_line=None):
        if from_line is None:
            self.__surname = surname
            self.__name = name
            self.__namb = namb
            self.__bd = bd
            self.__adrs = adrs
        else:
            self.surname, self.name, self.namb, self.bd, self.adrs = str(from_line).replace(" ", '').split(";")

    @property
    def surname(self):
        return self.__surname

    @surname.setter
    def surname(self, surname):
        self.__surname = surname

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, name):
        self.__name = name

    @property
    def namb(self):
        return self.__namb

    @namb.setter
    def namb(self, namb):
        self.__namb = namb

    @property
    def bd(self):
        return self.__bd

    @bd.setter
    def bd(self, bd):
        self.__bd = bd

    @property
    def adrs(self):
        return self.__adrs

    @adrs.setter
    def adrs(self, adrs):
        self.__adrs = adrs

    def copy(self):
        return Member(self.surname, self.name, self.namb, self.bd, self.adrs)

    def __str__(self):
        return f'{self.surname} {self.name}, тел. {self.namb}, д.р. {self.bd}, адрес: {self.adrs}.'

    def __repr__(self):
        return f'{self.surname}; {self.name}; {self.namb}; {self.bd}; {self.adrs}'


import os


class Contacts:

    def __init__(self):
        self.__data_path = 'contacts.txt'
        self.__contact_list = []
        self.__load_contact_list()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.__save_contact_list()

    def __len__(self):
        return len(self.contact_list)

    def __load_contact_list(self):
        if os.path.isfile(self.__data_path) is True:
            with open(self.__data_path, 'rt', encoding='utf-8') as file:
                for line in file:
                    member = Member(from_line=line.strip())
                    self.contact_list.append(member)
        print(f'Количество загруженных записей: ', self.__len__())

    def __save_contact_list(self):
        with open(self.__data_path, 'wt', encoding='utf-8') as file:
            for m in self.contact_list:
                file.write(f'{repr(m)}\n')
        print(f'Количество сохраненных записей: ', self.__len__())

    @property
    def contact_list(self):
        return self.__contact_list

    @contact_list.setter
    def contact_list(self, contact_list):
        self.__contact_list = contact_list

    def add_member(self, member: Member):
        match_by_name = self.__get_match_member_by_name(member.surname, member.name)
        match_by_namber = self.__get_match_member_by_namber(member.namb)

        if match_by_name is not None:
            print('Запись не добавлена!!!')
            if match_by_namber is None:
                print('Контакт с таким именем уже существует:')
                print(match_by_name)
                return
            print('Контакт с таким именем и номером уже существует:')
            print(match_by_name)
            return
        elif match_by_namber is not None:
            print('Запись не добавлена!!!' + \
                  'Контакт с таким номером телефона уже существует:')
            print(match_by_namber)
            return
        self.contact_list.append(member)
        print(f'Добавлен контакт: ', member)
        return member

    def __get_match_member_by_name(self, surname, name):
        for member in self.contact_list:
            if (member.surname, member.name) == (surname, name):
                return member

    def __get_match_member_by_namber(self, namb):
        for member in self.contact_list:
            if member.namb == namb:
                return member

    # def find_member(self, surname, name, namb):
    #     if (surname, name, namb) == ("", "", ""):
    #         print("\nНевозможно осуществить поиск - критерии поиска не заданы!")
    #         return
    #     idx_list = []
    #     for idx, member in enumerate(self.contact_list):
    #         if member.name.lower().find(name.lower()) >= 0:
    #             if member.surname.lower().find(surname.lower()) >= 0:
    #                 if member.namb.lower().find(namb.lower()) >= 0:
    #                     idx_list.append(idx)
    #     return idx_list

    def find_member_with_mask(self, surname, name, namb):
        if (surname, name, namb) == ("", "", ""):
            print("Невозможно осуществить поиск - критерии поиска не заданы!")
            return
        idx_list = []
        for idx, member in enumerate(self.contact_list):
            if surname.find('*') >= 0 and member.surname.lower().find(surname.lower().split('*')[0]) == 0 or \
                    surname.find('*') < 0 and member.surname.lower().find(surname.lower()) >= 0:
                if name.find('*') >= 0 and member.name.lower().find(name.lower().split('*')[0]) == 0 or \
                        name.find('*') < 0 and member.name.lower().find(name.lower()) >= 0:
                    if namb.find('*') >= 0 and member.namb.lower().find(namb.lower().split('*')[0]) == 0 or \
                            namb.find('*') < 0 and member.namb.lower().find(namb.lower()) >= 0:
                        idx_list.append(idx)
        return idx_list

    def remove_member(self, idx):
        del self.contact_list[idx]

    def edit_member(self, new_member: Member, idx):
        match_by_name = None
        match_by_namber = None
        if self.contact_list[idx].name != new_member.name or self.contact_list[idx].surname != new_member.surname:
            match_by_name = self.__get_match_member_by_name(new_member.surname, new_member.name)
        if self.contact_list[idx].namb != new_member.namb:
            match_by_namber = self.__get_match_member_by_namber(new_member.namb)
        if match_by_name is not None:
            print('Запись не добавлена!!!')
            if match_by_namber is None:
                print('Контакт с таким именем уже существует:')
                print(match_by_name)
                return
            print('Контакт с таким именем и номером уже существует:')
            print(match_by_name)
            return
        elif match_by_namber is not None:
            print('Запись не добавлена!!!' + \
                  'Контакт с таким номером телефона уже существует:')
            print(match_by_namber)
            return
        self.contact_list[idx] = new_member
        print(f'Контакт изменен: ', new_member)
        return new_member

    def sort_contacts(self, by_surname=True, reverse=False):
        if by_surname is True:
            self.contact_list.sort(reverse=reverse, key=lambda member: f"{member.surname}")
        else:
            self.contact_list.sort(reverse=reverse, key=lambda member: f"{member.name}")

    def show_contacts_by_idx(self, idx_list):
        for i, idx in enumerate(idx_list):
            print(f'{i + 1}.', self.contact_list[idx])

    def show_all_contacts(self):
        for i, member in enumerate(self.contact_list):
            print(f'{i + 1}.', member)


def main_menu():
    selector = None
    try:
        selector = int(input('_' * 42 + '\n' \
                                        '|__________________МЕНЮ__________________|\n' + \
                             'Введите "1" если хотите добавить новый контакт\n' + \
                             'Введите "2" если хотите найти контакт\n' + \
                             'Введите "3" если хотите удалить контакт\n' + \
                             'Введите "4" если хотите изменить контакт\n' + \
                             'Введите "5" если хотите отсортировать записи\n' + \
                             'Введите "6" если хотите просмотреть все записи\n' + \
                             'Введите "7" если хотите сохранить и выйти\n' + \
                             '******************************************\n'
                             'Сделайте Ваш выбор -->:'))
    except ValueError:
        print('Некорректный ввод!!!')
        print('Необходимо ввести целое число!!!')
    return selector


def is_empty(contacts):
    if len(contacts) == 0:
        print("Список контактов пуст, записей нет!")
        return True
    return False


def add_execution(contacts):
    while True:
        print("_______Добавление новой записи:_______")
        print("Доступны следующие поля: фамилия*, имя*, телефон*, дата рождения, адрес.")
        print("Поля отмеченные * обязательны для заполнения.")
        surname = input("Введите фамилию*: ").strip().capitalize()
        name = input("Введите имя*: ").strip().capitalize()
        namb = input("Введите номер телефона*: ").strip()
        bd = input("Введите дату рождения: ").strip()
        adrs = input("Введите адрес: ").strip()

        success_flag = True
        if len(surname) == 0:
            success_flag = False
            print("Поле фамилии не может быть пустым!")
        if len(name) == 0:
            success_flag = False
            print("Поле имени не может быть пустым!")
        if len(namb) == 0:
            success_flag = False
            print("Поле номера телефона не может быть пустым!")
        if success_flag is True:
            m = Member(surname, name, namb, bd, adrs)
            contacts.add_member(m)

        selector = None
        try:
            selector = int(input(
                '\nВведите "1" чтобы добавить новую запись\n' + \
                'Введите другое, чтобы вернуться\n' + \
                'Сделайте Ваш выбор -->:'))
        except ValueError:
            print('\nНекорректный ввод, необходимо ввести целое число!!!')
            pass
        if selector == 1:
            continue
        else:
            return


def search_execution(contacts):
    while True:
        print("\n_______Поиск записей:_______")
        if is_empty(contacts) is True:
            return
        print("Доступны следующие критерии поиска: фамилия*, имя*, телефон*.")
        print("Для поиска введите один или несколько критериев (от одного символа и более).")
        print("Остальное можете пропустить нажав Enter.")
        print("* - используйте маску, если необходим поиск по начальной послеовательности символов.")
        surname = input('Для поиска контакта введите его фамилию: ').strip()
        name = input('Для поиска контакта введите его имя: ').strip()
        namb = input('Для поиска контакта введите его номер телефона: ').strip()
        find_result = contacts.find_member_with_mask(surname, name, namb)
        if find_result is not None:
            print("Результат поиска:")
            if len(find_result) == 0:
                print("Соответствий не найдено!")
            else:
                contacts.show_contacts_by_idx(find_result)
        selector = None
        try:
            selector = int(input(
                '\nВведите "1" чтобы ввести новые критерии поиска\n' + \
                'Введите другое, чтобы продолжить\n' + \
                'Сделайте Ваш выбор -->:'))
        except ValueError:
            print('\nНекорректный ввод, необходимо ввести целое число!!!')
            pass
        if selector == 1:
            continue
        else:
            return find_result


def sort_execution(contacts):
    print("\n_______Сортировка записей:_______")
    if is_empty(contacts) is True:
        return
    selector = None
    try:
        selector = int(input(
            'Введите "1" чтобы отсортировать записи по фамилии в алфавитном порядке\n' + \
            'Введите "2" чтобы отсортировать записи по фамилии в обратном порядке\n' + \
            'Введите "3" чтобы отсортировать записи по имени в алфавитном порядке\n' + \
            'Введите "4" чтобы отсортировать записи по имени в обратном порядке\n' + \
            'Введите другое, чтобы вернуться\n' + \
            '\n' \
            'Сделайте Ваш выбор -->:'))
    except ValueError:
        print('\nНекорректный ввод, необходимо ввести целое число!!!')
        pass
    if selector == 1:
        print("Идет процесс сортировки контактов по фамилии в алфавитном порядке ...")
        contacts.sort_contacts(by_surname=True, reverse=False)
        print("Контакты успешно отсортированы по фамилии в алфавитном порядке!")
    elif selector == 2:
        print("Идет процесс сортировки контактов по фамилии в обратном порядке ...")
        contacts.sort_contacts(by_surname=True, reverse=True)
        print("Контакты успешно отсортированы по фамилии в обратном порядке!")
    elif selector == 3:
        print("Идет процесс сортировки контактов по имени в алфавитном порядке ...")
        contacts.sort_contacts(by_surname=False, reverse=False)
        print("Контакты успешно отсортированы по имени в алфавитном порядке!")
    elif selector == 4:
        print("Идет процесс сортировки контактов по имени в обратном порядке ...")
        contacts.sort_contacts(by_surname=False, reverse=True)
        print("Контакты успешно отсортированы по имени в обратном порядке!")
    else:
        print('Сортировка не выбрана!')


def remove_execution(contacts):
    while True:
        print("\n_______Удаление записи:_______")
        if is_empty(contacts) is True:
            return
        selector = None
        try:
            selector = int(input(
                'Введите "1" чтобы воспользоваться поиском\n' + \
                'Введите "2" чтобы отобразить все записи\n' + \
                'Введите другое, чтобы вернуться\n' + \
                '******************************************\n'
                'Сделайте Ваш выбор -->:'))
        except ValueError:
            print('\nНекорректный ввод, необходимо ввести целое число!!!')
            pass
        if selector == 1:
            find_result = search_execution(contacts)
        elif selector == 2:
            show_all_execution(contacts)
            find_result = range(len(contacts.contact_list))
        else:
            return

        if find_result is not None:
            if len(find_result) == 0:
                ent = input("Для продолжения нажмите Enter ... ")
                continue

            ent_idx = input('******************************************'
                            '\nУкажите порядковый номер записи для удаления' + \
                            '\nДля отмены нажмите Enter' + \
                            '\n******************************************'
                            '\nСделайте Ваш выбор -->:')
            try:
                ent_idx = int(ent_idx)
                if 0 <= ent_idx - 1 < len(find_result):
                    removed_member = contacts.contact_list[find_result[ent_idx - 1]]
                    contacts.remove_member(find_result[ent_idx - 1])
                    print(f"Следующая запись удалена:\n{ent_idx}. {removed_member}")
                    ent = input("Для продолжения нажмите Enter ... ")
                else:
                    print(f"Запись под номером {ent_idx} не найдена!")
            except ValueError:
                print("Удаление отменено пользователем!")
                ent = input("Для продолжения нажмите Enter ... ")
            continue
        ent = input("Для продолжения нажмите Enter ... ")


def edit_execution(contacts):
    while True:
        print("\n_______Редактирование записи:_______")
        if is_empty(contacts) is True:
            return
        selector = None
        try:
            selector = int(input(
                'Введите "1" чтобы воспользоваться поиском\n' + \
                'Введите "2" чтобы отобразить все записи\n' + \
                'Введите другое, чтобы вернуться\n' + \
                '******************************************\n'
                'Сделайте Ваш выбор -->:'))
        except ValueError:
            print('\nНекорректный ввод, необходимо ввести целое число!!!')
            pass
        if selector == 1:
            find_result = search_execution(contacts)
        elif selector == 2:
            show_all_execution(contacts)
            find_result = range(len(contacts.contact_list))
        else:
            return

        if find_result is not None:
            if len(find_result) == 0:
                ent = input("Для продолжения нажмите Enter ... ")
                continue

            ent_idx = input('******************************************'
                            '\nУкажите порядковый номер записи для редактирования' + \
                            '\nДля отмены нажмите Enter' + \
                            '\n******************************************'
                            '\nСделайте Ваш выбор -->:')
            try:
                ent_idx = int(ent_idx)
                if 0 <= ent_idx - 1 < len(find_result):
                    while True:
                        new_member = contacts.contact_list[find_result[ent_idx - 1]].copy()
                        print(f"\nВы редактируете следующую запись:\n{ent_idx}. {new_member}")
                        selector = None
                        try:
                            selector = int(input(
                                '******************************************\n'
                                'Введите "1" чтобы изменить фамилию\n' + \
                                'Введите "2" чтобы изменить имя\n' + \
                                'Введите "3" чтобы изменить номер телефона\n' + \
                                'Введите "4" чтобы изменить дату рождения\n' + \
                                'Введите "5" чтобы изменить адрес\n' + \
                                'Введите другое, чтобы вернуться назад\n' + \
                                '******************************************\n'
                                'Сделайте Ваш выбор -->:'))
                        except ValueError:
                            print('\nНекорректный ввод, необходимо ввести целое число!!!')
                            break

                        if selector == 1:
                            surname = input("Введите новую фамилию: ").strip().capitalize()
                            if len(surname) > 0:
                                new_member.surname = surname
                                contacts.edit_member(new_member, find_result[ent_idx - 1])
                            else:
                                print("Поле фамилии не может быть пустым!")
                        elif selector == 2:
                            name = input("Введите новое имя: ").strip().capitalize()
                            if len(name) > 0:
                                new_member.name = name
                                contacts.edit_member(new_member, find_result[ent_idx - 1])
                            else:
                                print("Поле имени не может быть пустым!")
                        elif selector == 3:
                            namb = input("Введите новый номер телефона: ").strip()
                            if len(namb) > 0:
                                new_member.namb = namb
                                contacts.edit_member(new_member, find_result[ent_idx - 1])
                            else:
                                print("Поле номера телефона не может быть пустым!")
                        elif selector == 4:
                            bd = input("Введите новую дату рождения: ").strip()
                            new_member.bd = bd
                            contacts.edit_member(new_member, find_result[ent_idx - 1])
                        elif selector == 5:
                            adrs = input("Введите новый адрес: ").strip()
                            new_member.adrs = adrs
                            contacts.edit_member(new_member, find_result[ent_idx - 1])
                        else:
                            pass
                        ent = input("Для продолжения нажмите Enter ... ")

                else:
                    print(f"Запись под номером {ent_idx} не найдена!")
            except ValueError:
                print("Редактирование отменено пользователем!")
                ent = input("Для продолжения нажмите Enter ... ")
            continue
        ent = input("Для продолжения нажмите Enter ... ")


def show_all_execution(contacts):
    print("\n_______Список контактов:_______")
    if is_empty(contacts) is True:
        return
    contacts.show_all_contacts()


print('Идет загрузка контактов ...')
with  Contacts() as contacts:
    while True:
        selector = main_menu()
        if selector == 1:
            add_execution(contacts)
            ent = input("Для возврата в главное меню нажмите Enter ... ")
        elif selector == 2:
            search_execution(contacts)
            ent = input("Для возврата в главное меню нажмите Enter ... ")
        elif selector == 3:
            remove_execution(contacts)
            ent = input("Для возврата в главное меню нажмите Enter ... ")
        elif selector == 4:
            edit_execution(contacts)
            ent = input("Для возврата в главное меню нажмите Enter ... ")
        elif selector == 5:
            sort_execution(contacts)
            ent = input("Для возврата в главное меню нажмите Enter ... ")
        elif selector == 6:
            show_all_execution(contacts)
            ent = input("Для возврата в главное меню нажмите Enter ... ")
        elif selector == 7:
            print("Сохранение и выход ...")
            break
