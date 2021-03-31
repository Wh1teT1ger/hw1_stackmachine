# HW №1 - Stack Machine  
  
### Выполнил: Бурылов Денис

* compiler.py - компиляция forth-кода из файла
* stackMachine.py - реализация Stack Machine
* vm.py - запуск forth-программы из файла

Набор инструкций Stack Machine:  
* int-арифметика: `%`, `*`, `+`, `-`, `/`, `==`
* преобразование в int, str: cast_int, cast_str
* drop - удалить TOS
* dup - дубликация TOS
* if - `true_clause false_clause condition if`
* jmp - переход на заданный адрес инструкции
* stack - вывести содержимое DS, IP, RS
* swap - поменять местами TOS, TOS-1
* print/println - вывести TOS
* read - прочитать ввод от user и положить в TOS
* call - вызов процедуры (сохранить состояние IP, перейти по адресу первой инструкции процедуры)
* return - возврат из процедуры (return_stack.pop)
* exit - завершение VM
* store - положить по имени TOS значение TOS-1
* load - загрузить содержимое переменной TOS, положить в TOS

Дополнительная инструкция:
* get_pointer - получить указатель и положить в TOS

Forth-программа - нахождения факториала

factorial.txt:
```
: get_arg print read cast_int ;

// store n
"Give me $n" get_arg "n" store
// store counter
"n" load 1 - "counter" store
// store a pointer to the beginning of the loop
get_pointer 4 + "pointer" store
// loop
"n" load "counter" load * "n" store
"counter" load 1 - "counter" store
// condition
"counter" load 0 =="pointer" load get_pointer 4 +  if jmp
"n! =" print "n" load print
```
