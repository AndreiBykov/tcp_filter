# Установка BCC  
Перед тем как приступить к установке BCC необходимо убедиться, что текущее ядро системы поддерживает работу с BCC.
Для работы с BCC необходимо ядро Linux версии от 4.1 и выше.
Чтобы просмотреть текущую версию установленного ядра необходимо выполнить команду:

`uname -r`

Помимо этого ядро должно быть сконфигурировано со следующими флагами:  
```
CONFIG_BPF=y  
CONFIG_BPF_SYSCALL=y
CONFIG_NET_CLS_BPF=m
CONFIG_NET_ACT_BPF=m
CONFIG_BPF_JIT=y
CONFIG_HAVE_BPF_JIT=y
CONFIG_BPF_EVENTS=y
CONFIG_NET_SCH_SFQ=m
CONFIG_NET_ACT_POLICE=m
CONFIG_NET_ACT_GACT=m
CONFIG_DUMMY=m
CONFIG_VXLAN=m
```
Для проверки конфигурации ядра необходимо просмотреть файл `/proc/config.gz`
или `/boot/config-<kernel-version>`, в зависимости от дистрибутива.
При иной конфигурации ядра или ранней версии ядра, необходимо собрать новое ядро,
установив при этом нужные флаги конфигурации  
## Сборка ядра Linux
Для начала необходимо скачать исходники ядра Linux с сайта www.kernel.org. Подойдёт любая версия ядра начиная с 4.1.

Затем необходимо распаковать скачанный архив. Это можно сделать командой:

`tar --xz -xvf linux-<kernel-version>.tar.xz`

Затем необходимо сконфигурировать ядро. Это можно сделать самостоятельно или используя готовый конфигурационный файл,
находящийся в репозитории. Его необходимо поместить в папку с распакованным ядром с именем `.config`.
После этого необходимо запустить программу конфигурации:

`make olddefconfig`

Затем можно приступить непосредственно к сборке ядра. Для этого необходимо выполнить команду:

``make -j `getconf _NPROCESSORS_ONLN` deb-pkg LOCALVERSION=-custom``

Сборка ядра может занять длительное время, вплоть до нескольких часов. По окончанию сборки а папке,
в которой находится папка с исходниками ядра, будут находиться следующие файлы:
```
linux-firmware-image-<kernel-version>-custom_<kernel-version>-custom-1_amd64.deb
linux-headers-<kernel-version>-custom_<kernel-version>-custom-1_amd64.deb
linux-image-<kernel-version>-custom_<kernel-version>-custom-1_amd64.deb
linux-image-<kernel-version>-custom-dbg_<kernel-version>-custom-1_amd64.deb
linux-libc-dev_<kernel-version>-custom-1_amd64.deb
```
Все эти пакеты необходимо установить с помощью команд:
```
sudo dpkg -i linux-firmware-image-<kernel-version>-custom_<kernel-version>-custom-1_amd64.deb
sudo dpkg -i linux-libc-dev_<kernel-version>-custom-1_amd64.deb
sudo dpkg -i linux-headers-<kernel-version>-custom_<kernel-version>-custom-1_amd64.deb
sudo dpkg -i linux-image-<kernel-version>-custom-dbg_<kernel-version>-custom-1_amd64.deb
sudo dpkg -i linux-image-<kernel-version>-custom_<kernel-version>-custom-1_amd64.deb
```
По завершению установки пакетов необходимо перезагрузить компьютер. Для того чтобы убедиться,
что новое ядро было установлено необходимо выполнить команду:

`uname -r`
## Установка BCC
Когда ядро Linux настроено, можно приступить к установке BCC.
Рассмотрим установку BCC с использованием apt на Ubuntu. Для этого необходимо выполнить следующие команды:
```
sudo apt-key adv --keyserver keyserver.ubuntu.com --recv-keys 4052245BD4284CDD
echo "deb https://repo.iovisor.org/apt/$(lsb_release -cs) $(lsb_release -cs) main" | sudo tee /etc/apt/sources.list.d/iovisor.list
sudo apt-get update
sudo apt-get install bcc-tools libbcc-examples linux-headers-$(uname -r)
```
