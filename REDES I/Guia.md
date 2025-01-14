Prova de redes

    1 Criar as 5 VMS;
        1.1  Criar o Gateway;
            1.1.1 Configurar as regras do Firewall e acesso via SSH;
        1.2  Criar o DNS1;
        1.3  Criar o DNS2;
        1.4  Criar o WEB;
        1.5  Criar o UBUNTU;
    2 Configurar o DHCP;
        2.1  Instalar o DHCP no Gateway;
        2.2  Configurar o UBUNTU com DHCP;
    3 Configurar o DNS;
        3.1  Configurar o DNS1 e DNS2;
    4 Configurar o APACHE;
        4.1  Configura o APACHE na máquina WEB;
    5 Configurar o HTTPS;
        5.1  Configurar o HTTPS na máquina WEB;
    6 Configurar o FTP;
        6.1  Configurar o FTP na máquina WEB;
    7 Configurar o NFS;
        7.1  Configurar o servidor NFS na máquina WEB;
    8 Configurar o PROXY;
        8.1  Configurar o PROXY na máquina GATEWAY;



# Guia de Configuração de Infraestrutura de Rede

### Índice  
1. **Pré-requisitos e Observações Gerais**  
2. **Criação do Ambiente Virtual**  
3. **Configuração do Gateway e Firewall**  
4. **Configuração do Servidor DHCP no Gateway**  
5. **Configuração dos Servidores DNS**  
6. **Configuração da Máquina Web**  
7. **Testes e Validação** 

## 1. Pré-requisitos e Observações Gerais
- **Adaptador Host-Only**: Configure a placa de rede VirtualBox `Host-Only Ethernet Adapter` com o IP `200.50.100.1/24` e **desative o servidor DHCP**.
- **Acesso SSH**: Para acessar as máquinas enquanto o firewall está ativo, utilize os seguintes comandos:
  - **Gateway**: `ssh -p 51000 aluno@200.50.100.2`
  - **DNS1**: `ssh -p 52000 aluno@200.50.100.2`
  - **DNS2**: `ssh -p 53000 aluno@200.50.100.2`
  - **Web**: `ssh -p 54000 aluno@200.50.100.2`

---

## 2. Criação do Ambiente Virtual

1. **Baixe as ISOs** das distribuições Debian e Ubuntu Server LTS.
2. **Configuração das Máquinas Virtuais**:
   - **Gateway**:
     - Adaptador 1: Modo `NAT`
     - Adaptador 2: Modo `Host-Only`, Nome: `VirtualBox Host-Only Ethernet Adapter`
     - Adaptador 3: Modo `Rede Interna`, Nome: `SRC1`
     - Instale o sistema e configure o IP manual: `172.16.100.1/24`

   - **DNS1**:
     - Adaptador 1: Rede Interna `SRC1`
   
   - **Web**:
     - Adaptador 1: Rede Interna `SRC1`
   
   - **DNS2**:
     - Clone linkado da máquina **DNS1**

---

## 3. Configuração do Firewall no Gateway

1. **Atualize o sistema**:
   ```bash
   sudo apt update && sudo apt upgrade -y
   ```

2. **Crie o script do firewall**:
   - Navegue até a pasta de configuração:
     ```bash
     mkdir ~/firewall && cd ~/firewall
     nano firewall
     ```
   - Adicione o conteúdo do script `firewall`:

     ```bash
     #!/bin/bash
     ### BEGIN INIT INFO
     # Provides:		firewall
     # Required-Start:	$syslog
     # Required-Stop:	$syslog
     # Default-Start:	2 3 4 5
     # Default-Stop:
     # Short-Description:	Firewall da Dexter
     ### END INIT INFO

     # Script de Firewall
     # Vagner Schoaba
     clear
     ### CORES
     VERDE="\033[1;32m"
     AMARELO="\033[1;33m"
     AZUL="\033[1;34m"
     VERMELHO="\033[1;31m"
     END="\033[m"
     ###
     ProgressBar() {
       tput civis
       for X in $(seq 20)
       do
         for i in ..
         do
           echo -en "\033[1D$i"
           #sleep .1
         done
       done
       tput cnorm
     }


     case $1 in
     stop)


     	# Definindo Politica ACCEPT - ACEITA TUDO
     	iptables -P OUTPUT ACCEPT
     	iptables -P INPUT ACCEPT
     	iptables -P FORWARD ACCEPT

     	# Limpar as Regras de todas as tableas
     	iptables -F
     	iptables -t nat -F
     	iptables -t mangle -F

     	iptables -t raw -F
     	iptables -t security -F

     	# Bloquear a passagem de pacotes pelo kernel
     	echo 0 > /proc/sys/net/ipv4/ip_forward
     	echo -en "Stopping Security Firewall Schoaba ";ProgressBar; echo -e " [\033[0;32m ok\033[m ]"

     ;;


     start)
     	$0 stop
     	sleep 0.5
     	echo -en "Starting Security Firewall Schoaba ";ProgressBar; echo -e " [\033[0;32m ok\033[m ]"
     	# liberar a passagem de pacotes pelo kernel
     	echo 1 > /proc/sys/net/ipv4/ip_forward

     	# Iniciando as Regras
     	bash /home/aluno/firewall/regras

     ;;


     restart)
     	$0 start
     ;;




     *)
     	echo 'POR FAVOR USE "stop|start|restart"'

     ;;

     esac
     ```

3. **Configuração de Regras de Firewall**:
   - Crie o arquivo de regras:
     ```bash
     nano regras
     ```
   - Adicione as regras de firewall:

     ```bash
     #!/bin/bash
     #INICIALIZACAO AUTOMATICA
     #ln -s /home/aluno/firewall.sh /etc/init.d
     #update-rc.d firewall defaults 3

     iptables -t nat -F
     iptables -F

     SSH=200.50.100.2
     SSH2=200.50.100.3
     GATEWAY=172.16.100.1
     DNS1=172.16.100.2
     DNS2=172.16.100.3
     WEB=172.16.100.4
     ARQUIVO=172.16.100.5
     AUTENTICACAO=172.16.100.6
     SAMBA=172.16.100.7
     EMAIL=172.16.100.8
     ALL=0/0

     LAN=172.16.100.0/24
     LOCAL=200.50.100.0/24

     echo "1" >/proc/sys/net/ipv4/ip_forward

     iptables -t nat -A POSTROUTING -s $LAN -j MASQUERADE

     ###### 1.0 - Gateway
     iptables -A FORWARD -p tcp -s $LOCAL -d $GATEWAY --dport 51000 -j ACCEPT
     iptables -A FORWARD -p tcp -s $GATEWAY -d $LOCAL --sport 22 -j ACCEPT
     iptables -t nat -A PREROUTING -p tcp -s $LOCAL -d $SSH --dport 51000 -j DNAT --to $GATEWAY:22

     ###### 2.0 - DNS1
     iptables -A FORWARD -p tcp -s $LOCAL -d $DNS1 --dport 52000 -j ACCEPT
     iptables -A FORWARD -p tcp -s $DNS1 -d $LOCAL --sport 22 -j ACCEPT

     iptables -t nat -A PREROUTING -p tcp -s $LOCAL -d $SSH --dport 52000 -j DNAT --to $DNS1:22


     ###### 2.1 - DNS1
     iptables -A FORWARD -p udp -s $DNS1 -d $LOCAL --sport 53 -j ACCEPT
     iptables -A FORWARD -p udp -s $LOCAL -d $DNS1 --dport 53 -j ACCEPT
     iptables -t nat -A PREROUTING -p udp -s $LOCAL -d $SSH --dport 53 -j DNAT --to $DNS1:53

     ###### 3.0 - DNS2
     iptables -A FORWARD -p tcp -s $LOCAL -d $DNS2 --dport 53000 -j ACCEPT
     iptables -A FORWARD -p tcp -s $DNS2 -d $LOCAL --sport 22 -j ACCEPT
     iptables -t nat -A PREROUTING -p tcp -s $LOCAL -d $SSH --dport 53000 -j DNAT --to $DNS2:22

     ###### 3.1 - DNS2
     iptables -A FORWARD -p udp -s $DNS2 -d $LOCAL --sport 53 -j ACCEPT
     iptables -A FORWARD -p udp -s $LOCAL -d $DNS2 --dport 53 -j ACCEPT
     iptables -t nat -A PREROUTING -p udp -s $LOCAL -d $SSH2 --dport 53 -j DNAT --to $DNS2:53

     ###### 3.2 - EMAIL SMTP

     iptables -A FORWARD -p tcp -s $LAN -m multiport --dports 25,110,143,587,993,995 -j ACCEPT

     iptables -A FORWARD -p tcp -s $SSH2 -d $EMAIL -m multiport --dports 25,110,143,587,993,995 -j ACCEPT


     ###### 4.0 - WEB
     iptables -A FORWARD -p tcp -s $LOCAL -d $WEB --dport 54000 -j ACCEPT
     iptables -A FORWARD -p tcp -s $WEB -d $LOCAL --sport 22 -j ACCEPT
     iptables -t nat -A PREROUTING -p tcp -s $LOCAL -d $SSH --dport 54000 -j DNAT --to $WEB:22

     ###### 5.0 - ARQUIVO
     iptables -A FORWARD -p tcp -s $LOCAL -d $ARQUIVO --dport 55000 -j ACCEPT
     iptables -A FORWARD -p tcp -s $ARQUIVO -d $LOCAL --sport 22 -j ACCEPT
     iptables -t nat -A PREROUTING -p tcp -s $LOCAL -d $SSH --dport 55000 -j DNAT --to $ARQUIVO:22


     ###### 6.0 - AUTENTICACAO
     iptables -A FORWARD -p tcp -s $LOCAL -d $AUTENTICACAO --dport 56000 -j ACCEPT
     iptables -A FORWARD -p tcp -s $AUTENTICACAO -d $LOCAL --sport 22 -j ACCEPT
     iptables -t nat -A PREROUTING -p tcp -s $LOCAL -d $SSH --dport 56000 -j DNAT --to $AUTENTICACAO:22
     iptables -A OUTPUT -p tcp -s $GATEWAY -d $AUTENTICACAO --dport 389 -j ACCEPT

     ###### 7.0 - SAMBA
     iptables -A FORWARD -p tcp -s $LOCAL -d $SAMBA --dport 57000 -j ACCEPT
     iptables -A FORWARD -p tcp -s $SAMBA -d $LOCAL --sport 22 -j ACCEPT
     iptables -t nat -A PREROUTING -p tcp -s $LOCAL -d $SSH --dport 57000 -j DNAT --to $SAMBA:22

     ###### 8.0 - EMAIL
     iptables -A FORWARD -p tcp -s $LOCAL -d $EMAIL --dport 58000 -j ACCEPT
     iptables -A FORWARD -p tcp -s $EMAIL -d $LOCAL --sport 22 -j ACCEPT
     iptables -t nat -A PREROUTING -p tcp -s $LOCAL -d $SSH --dport 58000 -j DNAT --to $EMAIL:22

     ###EMail
     for MAIL in 25 110 143 587 993 995
     do
       iptables -t nat -A PREROUTING -p tcp -s $ALL -d $SSH2 --dport $MAIL -j DNAT --to $EMAIL:$MAIL
     done



     ```
     
4. **Tornar scripts executáveis**:
   ```bash
   chmod +x firewall regras
   ```

5. **Instale o iptables**:
   ```bash
   sudo apt install iptables -y
   ```

6. **Executar o firewall**:
   ```bash
   sudo ./firewall start
   ```

---

## 4. Configuração do DHCP no Gateway

1. **Instale o servidor DHCP**:
   ```bash
   sudo apt update && sudo apt install isc-dhcp-server -y
   ```

2. **Configure o arquivo `/etc/default/isc-dhcp-server`**:
   - Edite o arquivo:
     ```bash
     sudo nano /etc/default/isc-dhcp-server
     ```
   - Defina as interfaces:
     ```bash
     INTERFACESv4="enp0s9 enp0s10"
     INTERFACESv6=""
     ```

3. **Inicie e verifique o servidor DHCP**:
   ```bash
   sudo systemctl restart isc-dhcp-server.service
   sudo systemctl status isc-dhcp-server.service
   ```

4. **Acompanhar logs**:
   ```bash
   sudo tail -f /var/lib/dhcp/dhcpd.leases
   ```

---

## 5. Configuração das Máquinas DNS

### DNS1
1. **Configuração de IP fixo**:
   - Edite o arquivo `/etc/netplan/50-cloud-init.yaml`:
     ```yaml
     network:
         ethernets:
             enp0s3:
                 addresses:
                 - 172.16.100.2/24
                 nameservers:
                     addresses:
                     - 8.8.8.8
                     search:
                     - laboratorio.lan
                 routes:
                 - to: default
                   via: 172.16.100.1
         version: 2
     ```

2. **Atualize o sistema**:
   ```bash
   sudo apt update && sudo apt upgrade -y
   ```

3. **Configuração do resolv.conf**:
   ```bash
   sudo nano /etc/resolv.conf
   nameserver 8.8.8.8
   ```

### DNS2
1. **Defina o hostname**:
   ```bash
   sudo hostnamectl set-hostname dns2
   ```

2. **Configuração de IP fixo**:
   - Edite o arquivo `/etc/netplan/50-cloud-init.yaml` com o seguinte conteúdo:

     ```yaml
     network:
         ethernets:
             enp0s3:
                 addresses:
                 - 172.16.100.3/24
                 nameservers:
                     addresses:
                     - 8.8.8.8
                     search:
                     - laboratorio.lan
                 routes:
                 - to: default
                   via: 172.16.100.1
         version: 2
     ```

3. **Atualize o sistema**:
   ```bash
   sudo apt update && sudo apt upgrade -y
   ```

---

## 6. Configuração da Máquina Web

1. **Configuração de IP fixo**:
   - Edite o arquivo `/etc/netplan/50-cloud-init.yaml`:

     ```yaml
     network:
         ethernets:
             enp0s3:
                 addresses:
                 - 172.16.100.4/24
                 nameservers:
                     addresses:
                     - 8.8.8.8
                     search:
                     - laboratorio.lan
                 routes:
                 - to: default
                   via: 172.16.100.1
         version: 2
     ```

2. **Configuração do resolv.conf**:
   ```bash
   sudo nano /etc/resolv.conf
   nameserver 8.8.8.8
   ```

---

## 7. Aula sobre DNS

### Consulta Reversa
- No DNS, a consulta reversa é escrita na ordem inversa do IP. Por exemplo:
  - O endereço `172.16.100.0` vira `0.100.16.172`.

### Configurações no Gateway
1. **Atualize o sistema e instale o Bind9**:
   ```bash
   sudo apt update && sudo apt upgrade -y
   sudo apt install bind9
   ```

2. **Verifique os serviços ativos**:
   ```bash
   ss -ntpl
   ```

3. **Navegue para a pasta de configuração**:
   ```bash
   cd /etc/bind
   ```

4. **Faça backup de arquivos existentes**:
   ```bash
   sudo cp named.conf.default-zones named.conf.default-zones.bkp
   ```

5. **Edite as zonas no arquivo de configuração**:
   ```bash
   sudo nano named.conf.default-zones
   ```
   Adicione:
   ```bash
   zone "laboratorio.lan" {
           type master;
           file "/etc/bind/ifro/lab.db";
   };

   zone "100.16.172.in-addr.arp" {
           type master;
           file "/etc/bind/ifro/lab.rev";
   };
   ```

6. **Crie os arquivos de zona**:
   ```bash
   sudo mkdir ifro
   sudo cp db.127 ifro/
   sudo cp db.local ifro/
   sudo mv ifro/db.127 ifro/lab.rev
   sudo mv ifro/db.local ifro/lab.db
   ```

7. **Configure os arquivos de zona**:
   - **Arquivo `lab.db`**:
     ```bash
     sudo nano ifro/lab.db
     ```
     Conteúdo:
     ```bash
     ;
     ; BIND data file for local loopback interface
     ;
     $TTL    604800
     @       IN      SOA     laboratorio.lan. root.laboratorio.lan. (
                                  1         ; Serial
                             604800         ; Refresh
                              86400         ; Retry
                            2419200         ; Expire
                             604800 )       ; Negative Cache TTL
     ;
     @       IN      NS      laboratorio.lan.
     @       IN      A       172.16.100.2
     ns      IN      A       172.16.100.2
     web     IN      A       172.16.100.4
     www     IN      CNAME   web.laboratorio.lan.
     dns1    IN      CNAME   ns.laboratorio.lan.
     ```

   - **Arquivo `lab.rev`**:
     ```bash
     sudo nano ifro/lab.rev
     ```
     Conteúdo:
     ```bash
     ;
     ; BIND reverse data file for local loopback interface
     ;
     $TTL    604800
     @       IN      SOA     laboratorio.lan. root.laboratorio.lan. (
                                  1         ; Serial
                             604800         ; Refresh
                              86400         ; Retry
                            2419200         ; Expire
                             604800 )       ; Negative Cache TTL
     ;
     @       IN      NS      laboratorio.lan.
     2       IN      PTR     laboratorio.lan.
     4       IN      PTR     web.laboratorio.lan.
     ```

8. **Verifique a configuração dos arquivos**:
   ```bash
   sudo named-checkconf
   sudo named-checkzone laboratorio.lan ifro/lab.db
   sudo named-checkzone 100.16.172.in-addr.arp ifro/lab.rev
   ```

9. **Reinicie o Bind9 e teste o DNS**:
   ```bash
   sudo systemctl restart bind9
   ping laboratorio.lan
   ```

10. **Configurar o resolv.conf**:
    ```bash
    sudo nano /etc/resolv.conf
    ```
    Adicione:
    ```bash
    nameserver 172.16.100.2
    nameserver 8.8.8.8
    ```

**Observação**: Todos os computadores devem ter essa mesma configuração no arquivo `/etc/resolv.conf`.

---
Apenas copiar a resposta
