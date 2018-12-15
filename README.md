# tcp_filter

Скрипт с использованием BCC, который фильтрует TCP/IP пакеты, отправленные на 80 или 443 порт.
Выводит на экран адрес источника и адрес назначения.

## Использование  
Запуск скрипта:  
`sudo python tcp_filter.py`

По умолчанию скрипт использует сетевой интерфейс eth0.  
Запуск скрипт с использованием другого интерфейса:  
`sudo python tcp_filter.py -i wlp3s0`
  
Список доступных интерфейсов можно узнать при помощи утилиты `ifconfig`  
  
## Реализация  
1. Фильтрация пакетов происходит с помощью eBPF. Происходит подключение к сокету указанного интерфейса (eth0 по умолчанию). Пакеты, удовлетвлряющие условию фильтрации перенаправлятся в пользовательское пространство.  
2. Скрипт получает отфильтрованные необработанные пакеты и выводит на экран информацию об адресе источника и назначения.
