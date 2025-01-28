## Pré-requisitos e Observações Gerais
- **Adaptador Host-Only**: Configure a placa de rede VirtualBox `Host-Only Ethernet Adapter` com o IP `192.168.56.1/24` e **DESATIVE o servidor DHCP**.
- **Em cada máquina adicone a rede interna com mesmo nome da placa de rede host-only do virtual box**
- **Acesso SSH**: Para acessar as máquinas enquanto o firewall está ativo, utilize os seguintes comandos:
  - **Gateway**: `ssh -p 51000 aluno@192.168.56.2`
  - **DNS1**: `ssh -p 52000 aluno@192.168.56.2`
  - **DNS2**: `ssh -p 53000 aluno@192.168.56.2`
  - **Web**: `ssh -p 54000 aluno@192.168.56.2`

---
### **Prova de Redes I**

#### **Observação**
Caso haja erros ao iniciar uma VM utilizando o modo Host-Only, apague a configuração antiga e crie uma nova.

---

4. **Configuração de IP em `/etc/network/interfaces`:**
   
   `su root`

   `nano /etc/network/interfaces`
   
   ```bash
   allow-hotplug enp0s8
   iface enp0s8 inet static
   address 192.168.100.1/24

   allow-hotplug enp0s9
   iface enp0s9 inet static
   address 192.168.56.2/24
   ```

- Acesse via SSH: `ssh aluno@192.168.56.2`.
  
   - Organize os repositorios:
     ```bash
     nano /etc/apt/sources.list
     ```
  
     ```bash
     deb http://security.debian.org/debian-security bullseye-security main contrib non-free
     deb-src http://security.debian.org/debian-security bullseye-security main contrib non-free

     deb http://deb.debian.org/debian bullseye main contrib non-free
     deb-src http://deb.debian.org/debian bullseye main contrib non-free

     deb http://deb.debian.org/debian bullseye-updates main contrib non-free
     deb-src http://deb.debian.org/debian bullseye-updates main contrib non-free

     deb http://deb.debian.org/debian bullseye-backports main contrib non-free
     deb-src http://deb.debian.org/debian bullseye-backports main contrib non-free
     ```
     
6. **Instalar `sudo`:**
   - `apt update && apt install sudo`
   - Edite o grupo com: `nano /etc/group`
   - Clique em: `Alt + shift + 3`
   - Altere a linha 21 para: `sudo:x:27:aluno`
   - Salve e saia.

7. **Desligar a máquina:**
   ```bash
   /sbin/shutdown -h now
   ```

---

### **CONFIGURAÇÃO NO GATEWAY**
1. **Atualize o sistema:**
   ```bash
   sudo apt update
   ```

3. **Criação do Script de Firewall:**
   - Crie o diretório `~/firewall` e entre nele.
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

     SSH=192.168.56.2
     SSH2=192.168.56.3
     GATEWAY=192.168.100.1
     DNS1=192.168.100.2
     DNS2=192.168.100.3
     WEB=192.168.100.4
     ARQUIVO=192.168.100.5
     AUTENTICACAO=192.168.100.6
     SAMBA=192.168.100.7
     EMAIL=192.168.100.8
     ALL=0/0

     LAN=192.168.100.0/24
     LOCAL=192.168.56.0/24

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
     - Torne os arquivos executáveis:
     ```bash
     chmod +x firewall regras
     ```
        
4. **Instale o `iptables`:**
   ```bash
   sudo apt install iptables -y
   ```

5. **Automatize a execução do firewall:**
   ```bash
   sudo ln -s /home/aluno/firewall/firewall /etc/init.d
   sudo update-rc.d firewall defaults 3
   ```

6. **Execute o firewall:**
   ```bash
   sudo ./firewall start
   ```

7. **Verifique as regras do `iptables`:**
   ```bash
   sudo iptables -nL
   ```

8. **Teste a automação:**
   - Verifique se o firewall inicia automaticamente após reiniciar a máquina.
   
9. **Criação do Snapshot.**

---

### **Configuração do DNS1 (Servidor DNS)**
1. **Ubuntu Server CLI:**
   - **Adaptador 1:** Rede Interna (mesma do gateway).
   - **Configuração de IP fixo:**
     Edite o arquivo `sudo nano /etc/netplan/50-cloud-init.yaml`:
     ```yaml
     network:
       version: 2
       ethernets:
         enp0s3:
           dhcp4: false
           addresses:
             - 192.168.100.2/24
           nameservers:
             addresses:
               - 8.8.8.8
             search:
               - prova.lan
           routes:
             - to: default
               via: 192.168.100.1
     ```
   - Aplique a configuração:
   ```bash
   sudo netplan apply
   ```

   - Teste acesso via ssh:
   ```bash
   ssh -p 52000 aluno@192.168.56.2
   ```

   **Se funcionar faça Snapshot da configuração de rede concluída**

2. **Instale e configure o BIND9 (DNS):**
   ```bash
   sudo apt update && sudo apt install bind9 -y
   ```

3. **Configure os arquivos do BIND9:**
   Edite `/etc/bind/named.conf.local` para adicionar as zonas:
   ```bash
   zone "prova.lan" {
           type master;
           file "/etc/bind/ifro/prova.db";
           allow-transfer { 192.168.100.3; };
   };

   zone "mylena.lab" {
           type master;
           file "/etc/bind/ifro/mylena.db";
           allow-transfer { 192.168.100.3; };
   };

   zone "100.16.172.in-addr.arpa" {
           type master;
           file "/etc/bind/ifro/mylena-prova.rev";
           allow-transfer { 192.168.100.3; };
   };
   ```

4. **Criação e configuração das zonas e arquivos de DNS:**
   - Crie o diretório `ifro` e copie os arquivos necessários.
   ```bash
   cd /etc/bind
   ```
   ```bash
   sudo mkdir ifro
   ```
   ```bash
   cd ifro
   ```
   ```bash
   sudo nano prova.db
   ```

   ```bash
   ;
   ; BIND data file for local loopback interface
   ;
   $TTL    604800
   @       IN      SOA     prova.lan. root.prova.lan. (
                   1         ; Serial
                   604800    ; Refresh
                   86400     ; Retry
                   2419200   ; Expire
                   604800 )  ; Negative Cache TTL
   ;
   @       IN      NS      prova.lan.
   @       IN      A       192.168.100.2
   ns      IN      A       192.168.100.2
   ava     IN      A       192.168.100.4
   www     IN      A       192.168.100.4
   ftp     IN      A       192.168.100.4
   dns1    IN      CNAME   ns.prova.lan.
   ```

   ```bash
   sudo nano mylena.db
   ```

   ```bash
   ;
   ; BIND data file for local loopback interface
   ;
   $TTL    604800
   @       IN      SOA     mylena.lab. root.prova.lab. (
                   1         ; Serial
                   604800    ; Refresh
                   86400     ; Retry
                   2419200   ; Expire
                   604800 )  ; Negative Cache TTL
   ;
   @       IN      NS      mylena.lab.
   @       IN      A       192.168.100.2
   ns      IN      A       192.168.100.2
   site    IN      A       192.168.100.4
   web     IN      A       192.168.100.4
   ```

   ```bash
   sudo nano mylena-prova.rev
   ```

   ```bash
   ;
   ; BIND reverse data file for local loopback interface
   ;
   $TTL    604800
   @       IN      SOA     prova.lan. root.prova.lan. (
                   1         ; Serial
                   604800    ; Refresh
                   86400     ; Retry
                   2419200   ; Expire
                   604800 )  ; Negative Cache TTL
   ;
   @       IN      NS      prova.lan.
   2       IN      PTR     prova.lan.
   4       IN      PTR     ava.prova.lan.
   4       IN      PTR     www.prova.lan.
   2       IN      PTR     mylena.lab
   4       IN      PTR     web.mylena.lab
   4       IN      PTR     site.mylena.lab
   ```
  
5. **Verifique a configuração do BIND9:**
   ```bash
   sudo named-checkconf
   sudo named-checkzone prova.lan prova.db
   sudo named-checkzone mylena.lab mylena.db
   sudo named-checkzone 100.16.172.in-addr.arpa mylena-prova.rev
   ```
   
2. Teste as resoluções:
   ```bash
   nslookup ava.prova.lan
   nslookup www.prova.lan
   nslookup web.mylena.lab
   nslookup site.mylena.lab
   ```
   
**Defina o DNS:**

```bash
sudo nano /etc/systemd/resolved.conf
```
```bash
[Resolve]
DNS=192.168.100.2 192.168.100.3 8.8.8.8
Domains=prova.lan
```
```bash
sudo rm /etc/resolv.conf
```

6. **Configurar o named.conf.options**
   ```bash
   sudo nano /etc/bind/named.conf.options
   ```
   ```bash
   options {
           directory "/var/cache/bind";
           forwarders {
                   8.8.8.8;
           };
           dnssec-validation auto;
           listen-on-v6 { any; };
   };
      ```

7. **Reinicie o serviço do BIND9:**
   ```bash
   sudo systemctl restart bind9
   sudo systemctl status bind9
   ```

8. **Teste o DNS com o comando `ping prova.lan`.**

**Salve o SNAPSHOT do DNS**

### **Configuração do DHCP**
1. **Acesse via SSH o DNS1:**
   ```bash
   ssh -p 52000 aluno@192.168.56.2
   ```

2. **Instalar e configurar o servidor DHCP:**
   ```bash
   sudo apt update && sudo apt install isc-dhcp-server -y
   ```

3. **Configurar o arquivo `/etc/default/isc-dhcp-server`:**
   ```bash
   INTERFACESv4="enp0s3"
   ```

4. **Configuração do arquivo `/etc/dhcp/dhcpd.conf`:**
   Adicione a configuração de rede:
   ```bash
   subnet 192.168.100.0 netmask 255.255.255.0 {
     range 192.168.100.50 192.168.100.70;
     option domain-name-servers 192.168.100.2, 192.168.100.3, 8.8.8.8;
     option domain-name "prova.lan";
     option routers 192.168.100.1;
     option broadcast-address 192.168.100.255;
     default-lease-time 600;
     max-lease-time 7200;
   }
   ```

### **Configuração do Ubuntu**
1. **Adaptador 1:** Rede Interna `intnet`.

  - Instale o ubuntu normalmente sem internet.

5. **Tente executar o comando `ping prova.lan`**

6. **Desligue a máquina e crie o Snapshot da máquina DNS1 e Ubuntu.**

---

### **Configuração do DNS2**

**Definir o /etc/hosts:**
   ```bash
   sudo nano /etc/hosts
   ```
   ```bash
   127.0.0.1 localhost
   127.0.1.1 dns2
   192.168.100.3    dns2    dns2.prova.lan
   192.168.100.2    dns1    dns1.prova.lan
   192.168.100.1    gateway gateway.prova.lan

   # The following lines are desirable for IPv6 capable hosts
   ::1     ip6-localhost ip6-loopback
   fe00::0 ip6-localnet
   ff00::0 ip6-mcastprefix
   ff02::1 ip6-allnodes
   ff02::2 ip6-allrouters
   ```

3. **Configuração de IP Fixo:**
   - Edite o arquivo `/etc/netplan/50-cloud-init.yaml` com o seguinte conteúdo:
   ```yaml
   network:
     version: 2
     ethernets:
       enp0s3:
         dhcp4: false
         addresses:
           - 192.168.100.3/24
         nameservers:
           addresses:
             - 8.8.8.8
           search:
             - prova.lan
         routes:
           - to: default
             via: 192.168.100.1
   ```

   ```bash
   sudo rm /etc/resolv.conf
   ```

   - Aplique a configuração:
   ```bash
   sudo netplan apply
   ```

**Configurar o Resolvedor Local**
1. Certifique-se de que o DNS2 também aponta para o DNS1. Edite o arquivo do resolvedor:
   ```bash
   sudo nano /etc/systemd/resolved.conf
   ```
2. Adicione ou edite as seguintes linhas:
   ```plaintext
   [Resolve]
   DNS=192.168.100.2 8.8.8.8
   Domains=prova.lan
   ```

3. Reinicie o resolvedor para aplicar as mudanças:
   ```bash
   sudo systemctl restart systemd-resolved
   ```
   
3. **Reiniciar e Verificar Conexão:**
   - Reinicie a máquina:
   ```bash
   sudo reboot
   ```
   - Teste o IP, ping para `prova.lan`.
   - Desligue a máquina e crie um snapshot.

### Configuração do DNS2 como Slave no Bind9

#### **Passo 1: Instalar o Bind9 no DNS2**
1. Instale o Bind9:
   ```bash
   sudo apt update && sudo apt install bind9 -y
   ```

---

#### **Passo 2: Configurar as Zonas no DNS2**
1. Edite o arquivo de zonas padrão do Bind:
   ```bash
   sudo nano /etc/bind/named.conf.local
   ```
2. Adicione as configurações abaixo para criar as zonas **prova.lan** e a zona reversa **100.16.172.in-addr.arpa**:
   ```bash
   // Zona direta para prova.lan
   zone "prova.lan" {
       type slave;
       file "/etc/bind/ifro/prova.db"; // Caminho do arquivo de zona
       masters { 192.168.100.2; };    // IP do servidor master
   };

   zone "mylena.lab" {
       type slave;
       file "/etc/bind/ifro/mylena.db"; // Caminho do arquivo de zona
       masters { 192.168.100.2; };    // IP do servidor master
   };

   // Zona reversa para 192.168.100.0/24
   zone "100.16.172.in-addr.arpa" {
       type slave;
       file "/etc/bind/ifro/mylena-prova.rev"; // Caminho do arquivo de zona reversa
       masters { 192.168.100.2; };     // IP do servidor master
   };
   ```

---

#### **Passo 3: Criar Diretório para os Arquivos de Zona**
1. Crie o diretório onde os arquivos de zona serão armazenados:
   ```bash
   sudo mkdir -p /etc/bind/ifro
   ```

---

#### **Passo 5: Reiniciar o Serviço Bind9**
1. Reinicie o serviço Bind9 para carregar as novas configurações:
   ```bash
   sudo systemctl restart bind9
   ```

2. Verifique se o serviço está ativo:
   ```bash
   sudo systemctl status bind9
   ```
   Certifique-se de que o serviço está **"active (running)"**.

---

#### **Passo 6: Testar as Configurações**
1. Teste a resolução de nomes usando o **dig**:
   ```bash
   dig @192.168.100.3 prova.lan
   dig @192.168.100.3 -x 192.168.100.2
   ```

2. Se tudo estiver configurado corretamente, você verá as respostas das consultas apontando para o DNS1 como servidor mestre.

CRIE UM SNAPSHOT

### **Configuração do WEB**

1. **Configuração de IP Fixo:**
   - Edite o arquivo `/etc/netplan/50-cloud-init.yaml` com o seguinte conteúdo:
   ```yaml
   network:
     version: 2
     ethernets:
       enp0s3:
         dhcp4: false
         addresses:
           - 192.168.100.4/24
         nameservers:
           addresses:
             - 8.8.8.8
           search:
             - prova.lan
         routes:
           - to: default
             via: 192.168.100.1
   ```

   - Aplique a configuração:
   ```bash
   sudo netplan apply
   ```

2. **Configuração de DNS:**
   - Edite `/etc/systemd/resolved.conf`:
   ```ini
   [Resolve]
   DNS=192.168.100.2 192.168.100.3 8.8.8.8
   Domains=prova.lan
   ```
   ```bash
   sudo rm /etc/resolv.conf
   ```
   - Reinicie a máquina e verifique o IP, teste internet com `ping prova.lan`.
   - Desligue a máquina e crie um snapshot.


#### 3.1. Configurar o Apache na máquina WEB

- `ssh -p 54000 aluno@192.168.56.2`

Com base nos requisitos adicionais fornecidos, vou ajustar a configuração para garantir que:

1. A máquina WEB tenha **Apache com suporte a PHP**, **MySQL** e **PHPMyAdmin** instalados e configurados.
2. O servidor use exclusivamente HTTPS, com suporte a SSL, rejeitando conexões HTTP.
3. O servidor utilize o IP **192.168.100.4**, conforme especificado.
Fdp
---

### **Configuração Ajustada**

#### **1. Atualizar e instalar os pacotes necessários**
Execute os seguintes comandos para instalar o Apache, PHP, MySQL e PHPMyAdmin:

```bash
sudo apt update

# Instalar Apache, MySQL e PHP
sudo apt install apache2 mysql-server php libapache2-mod-php php-mysql php-cli -y

# Instalar PHPMyAdmin
sudo apt install phpmyadmin -y
```


#### **4. Configurar o PHPMyAdmin**
Durante a instalação do PHPMyAdmin:
- Escolha o servidor Apache2.
- Configure o banco de dados do PHPMyAdmin durante o processo de instalação.
- Mysql

#### **3. Configurar Apache para HTTPS e bloquear HTTP**
1. **Ativar o módulo SSL e criar um certificado autoassinado**:

```bash
sudo a2enmod ssl
sudo mkdir /etc/apache2/ssl

# Gerar um certificado autoassinado (válido por 1 ano)
sudo openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
  -keyout /etc/apache2/ssl/apache-selfsigned.key \
  -out /etc/apache2/ssl/apache-selfsigned.crt \
  -subj "/C=BR/ST=Estado/L=Cidade/O=Organizacao/CN=prova.lan"
```

6. Ajuste as permissões dos arquivos:
   ```bash
   sudo chmod 600 /etc/apache2/ssl/apache-selfsigned.key
   sudo chmod 600 /etc/apache2/ssl/apache-selfsigned.crt
   ```
   
2. **Configurar o Apache para forçar HTTPS**:
   Edite ou crie o arquivo de configuração `/etc/apache2/sites-available/prova.lan.conf` com o seguinte conteúdo:

```apache
# Redirecionar HTTP para HTTPS
<VirtualHost *:80>
    ServerName prova.lan
    Redirect permanent / https://prova.lan/
</VirtualHost>

# Configuração HTTPS
<VirtualHost *:443>
    ServerAdmin admin@prova.lan
    ServerName prova.lan

    DocumentRoot /srv/prova/ava/

    SSLEngine on
    SSLCertificateFile /etc/apache2/ssl/apache-selfsigned.crt
    SSLCertificateKeyFile /etc/apache2/ssl/apache-selfsigned.key

    ErrorLog ${APACHE_LOG_DIR}/error.log
    CustomLog ${APACHE_LOG_DIR}/access.log combined

    <Directory /srv/prova/ava/>
        Options Indexes FollowSymLinks
        AllowOverride All
        Require all granted
    </Directory>
</VirtualHost>
```

3. **Ativar a nova configuração e desativar HTTP**:
   
```bash
sudo a2ensite prova.lan.conf
sudo a2dissite 000-default.conf
sudo systemctl reload apache2
```

- 
Se necessário, reconfigure:

```bash
sudo dpkg-reconfigure phpmyadmin
```

```bash
sudo mkdir -p /srv/prova/phpmyadmin
```

```bash
sudo ln -s /usr/share/phpmyadmin /srv/prova/phpmyadmin
```

**NO DNS1 RODE:** 
```bash
sudo systemctl restart isc-dhcp-server
```



Verifique se o PHPMyAdmin está acessível pelo HTTPS na máquina ubuntu, **TODO ACESSO EM HTTPS, DEVE SER FEITO NA MÁQUINA UBUNTU COM INTERFACE GRAFICA**: `https://192.168.100.4/phpmyadmin`.

---

8. **Configurar o arquivo de configuração do Apache**:
    ```bash
    sudo nano /etc/apache2/apache2.conf
    ```
    - Adicionar a seguinte configuração:
      ```apache
      <Directory /srv/>
          Options Indexes FollowSymLinks
          AllowOverride None
          Require all granted
      </Directory>
      ```

#### **5. Configurar as entradas do Apache para os domínios**
Edite novamente o arquivo `/etc/apache2/sites-available/prova.lan.conf` para adicionar os blocos de configuração para cada domínio:

```apache
# ava.prova.lan
<VirtualHost *:443>
    ServerAdmin admin@prova.lan
    ServerName ava.prova.lan
    DocumentRoot /srv/prova/ava/moodle

    SSLEngine on
    SSLCertificateFile /etc/apache2/ssl/apache-selfsigned.crt
    SSLCertificateKeyFile /etc/apache2/ssl/apache-selfsigned.key

    ErrorLog ${APACHE_LOG_DIR}/ava_error.log
    CustomLog ${APACHE_LOG_DIR}/ava_access.log combined
</VirtualHost>

# www.prova.lan
<VirtualHost *:443>
    ServerAdmin admin@prova.lan
    ServerName www.prova.lan
    DocumentRoot /srv/prova/www

    SSLEngine on
    SSLCertificateFile /etc/apache2/ssl/apache-selfsigned.crt
    SSLCertificateKeyFile /etc/apache2/ssl/apache-selfsigned.key

    ErrorLog ${APACHE_LOG_DIR}/www_error.log
    CustomLog ${APACHE_LOG_DIR}/www_access.log combined
</VirtualHost>

# web.mylena.lab
<VirtualHost *:443>
    ServerAdmin admin@prova.lan
    ServerName web.mylena.lab
    DocumentRoot /srv/aula/web

    SSLEngine on
    SSLCertificateFile /etc/apache2/ssl/apache-selfsigned.crt
    SSLCertificateKeyFile /etc/apache2/ssl/apache-selfsigned.key

    ErrorLog ${APACHE_LOG_DIR}/web_error.log
    CustomLog ${APACHE_LOG_DIR}/web_access.log combined
</VirtualHost>

# site.mylena.lab
<VirtualHost *:443>
    ServerAdmin admin@prova.lan
    ServerName site.mylena.lab
    DocumentRoot /srv/aula/site

    SSLEngine on
    SSLCertificateFile /etc/apache2/ssl/apache-selfsigned.crt
    SSLCertificateKeyFile /etc/apache2/ssl/apache-selfsigned.key

    ErrorLog ${APACHE_LOG_DIR}/site_error.log
    CustomLog ${APACHE_LOG_DIR}/site_access.log combined
</VirtualHost>
```


Para seguir o guia e organizar os diretórios e arquivos conforme as especificações, aqui está o passo a passo para ser executado no terminal:

### 1. Criar os diretórios:
Primeiro, vamos criar os diretórios necessários no caminho especificado para os sites. Use os seguintes comandos:

```bash
sudo mkdir -p /srv/prova/www
sudo mkdir -p /srv/aula/web
sudo mkdir -p /srv/aual/site
```

### 2. Definir permissões:
Atribua as permissões adequadas aos diretórios, de modo que o servidor web tenha acesso para gravar e ler neles. Isso depende do servidor web que você está utilizando, mas geralmente é necessário garantir que o usuário do servidor web tenha permissões sobre esses diretórios. Por exemplo, se você estiver usando o Apache, o usuário do servidor web geralmente é `www-data`.

```bash
sudo chown -R www-data:www-data /srv/prova/www
sudo chown -R www-data:www-data /srv/aula/web
sudo chown -R www-data:www-data /srv/aual/site
```

### 3. Criar os arquivos HTML/PHP em cada diretório:
Agora, vamos criar o arquivo HTML/PHP em cada diretório com o conteúdo solicitado.

**Para /srv/prova/www:**

```bash
echo -e "<html>\n<center>\n<font size=5>\n<br><br><br>\n<?php\n echo getcwd() . \"\\n\";\n?>\n" | sudo tee /srv/prova/www/index.php > /dev/null
```

**Para /srv/aula/web:**

```bash
echo -e "<html>\n<center>\n<font size=5>\n<br><br><br>\n<?php\n echo getcwd() . \"\\n\";\n?>\n" | sudo tee /srv/aula/web/index.php > /dev/null
```

**Para /srv/aual/site:**

```bash
echo -e "<html>\n<center>\n<font size=5>\n<br><br><br>\n<?php\n echo getcwd() . \"\\n\";\n?>\n" | sudo tee /srv/aual/site/index.php > /dev/null
```

### 4. Verificar se os arquivos foram criados:
Após criar os arquivos, você pode verificar se eles foram criados corretamente com o seguinte comando:

2. Ative o site e os módulos necessários:
   ```bash
   sudo a2ensite web-ssl.conf
   sudo a2enmod ssl
   sudo a2enmod rewrite
   ```

```bash
cat /srv/prova/www/index.php
cat /srv/aula/web/index.php
cat /srv/aual/site/index.php
```

Esses comandos exibirão o conteúdo dos arquivos para que você possa verificar se está tudo correto.

### 6. Habilitar os sites e reiniciar o servidor:
Agora, ative as configurações dos sites e reinicie o servidor Apache:

```bash
sudo a2ensite prova.lan.conf
```


### **6. Testes**
1. **Verificar os serviços do Apache e MySQL**:
   ```bash
   sudo systemctl status apache2
   sudo systemctl status mysql
   ```

2. **Acessar os domínios configurados via HTTPS no navegador:**
   - `https://ava.prova.lan`
   - `https://www.prova.lan`
   - `https://web.mylena.lab`
   - `https://site.mylena.lab`

3. **Testar o PHPMyAdmin:**
   Acesse: `https://192.168.100.4/phpmyadmin`.

---


e salve SNAPSHOT**
---

**TESTE E CRIE SNAPSHOT**
---

## 5. Configuração do FTP

### 5.1 Configurações na máquina DNS1

1. **Editar o arquivo de zona do BIND**  
   Abra o arquivo de configuração do BIND para editar a zona do domínio `prova.lan`:
   ```bash
   sudo nano /etc/bind/ifro/prova.db
   ```

2. **Adicionar as configurações de DNS1**  
   Adicione ou edite as seguintes linhas no arquivo de zona:

   ```txt
   web     IN      A       192.168.100.4
   ftp     IN      A       192.168.100.4
   ```

3. **Reiniciar o serviço BIND**  
   Após editar o arquivo, reinicie o serviço BIND para aplicar as mudanças:
   ```bash
   sudo systemctl restart bind9
   ```

4. **Verificar a resolução DNS**  
   Use o comando `dig` para verificar se o servidor FTP (`ftp.prova.lan`) resolve corretamente para o IP `192.168.100.4`:
   ```bash
   dig ftp.prova.lan
   ```
   O retorno esperado deve ser:
   ```txt
   ;; ANSWER SECTION:
   ftp.prova.lan.       604800  IN  A  192.168.100.4
   ```

---

### 5.2 Configurações na máquina DNS2

1. **Instalar o ProFTPD**  
   Para instalar o servidor FTP ProFTPD, execute o seguinte comando:
   ```bash
   sudo apt install proftpd -y
   ```

2. **Criar o diretório FTP**  
   Crie o diretório onde os arquivos do FTP serão armazenados:
   ```bash
   sudo mkdir -p /sr/ftp
   ```

3. **Alterar a propriedade do diretório**  
   Modifique a propriedade do diretório para o usuário e grupo `aluno`:
   ```bash
   sudo chown aluno:aluno /sr/ftp
   ```

4. **Ajustar as permissões do diretório**  
   Defina as permissões adequadas para o diretório FTP:
   ```bash
   sudo chmod 755 /sr/ftp
   ```

5. **Configurar o ProFTPD**  
   Abra o arquivo de configuração do ProFTPD para definir o nome do servidor e o diretório raiz:
   ```bash
   sudo nano /etc/proftpd/proftpd.conf
   ```

   Adicione ou edite as seguintes linhas:
   ```txt
   ServerName "Laboratorio"
   # Use this to jail all users in their homes
   DefaultRoot /sr/ftp
   ```

6. **Reiniciar o ProFTPD**  
   Após as configurações, reinicie o serviço ProFTPD para aplicar as mudanças:
   ```bash
   sudo systemctl restart proftpd
   ```

---

### 5.3 Teste no WEB

1. **Testar a conexão FTP**  
   No Ubuntu, execute o comando FTP para testar a conexão com o servidor FTP configurado:
   ```bash
   ftp ftp.prova.lan
   ```
**TESTE E SALVE SNAPSHOT, NO DNS1 E WEB**
---

## 6. Configuração do NFS

### 6.1 Configurar o Servidor NFS na Máquina DNS2

1. **Atualizar o sistema**  
   Antes de instalar o NFS, é importante atualizar o sistema:
   ```bash
   sudo apt update
   ```

2. **Instalar o NFS Kernel Server**  
   Instale o pacote necessário para configurar o servidor NFS:
   ```bash
   sudo apt install nfs-kernel-server -y
   ```

3. **Criar o diretório compartilhado**  
   Crie o diretório que será compartilhado via NFS:
   ```bash
   sudo mkdir -p /srv/web
   ```

4. **Alterar a propriedade do diretório**  
   Defina a propriedade do diretório para o usuário `nobody` e grupo `nogroup`, que são comuns para compartilhamentos NFS:
   ```bash
   sudo chown nobody:nogroup /srv/web
   ```

5. **Ajustar as permissões do diretório**  
   Altere as permissões do diretório para permitir o acesso necessário:
   ```bash
   sudo chmod 755 /srv/web
   ```

6. **Configurar o arquivo de exportação**  
   Edite o arquivo `/etc/exports` para definir quais diretórios serão compartilhados e suas permissões. Abra o arquivo para edição:
   ```bash
   sudo nano /etc/exports
   ```

   Adicione a seguinte linha para permitir o acesso ao diretório `/srv/web` da rede `192.168.100.0/24` com permissões de leitura e gravação:
   ```txt
   /srv/web 192.168.100.0/24(rw,no_root_squash,sync)
   ```

7. **Reiniciar o serviço NFS**  
   Após a configuração, reinicie o serviço NFS para aplicar as mudanças:
   ```bash
   sudo systemctl restart nfs-kernel-server
   ```

8. **Verificar os compartilhamentos NFS**  
   Use o comando `exportfs -v` para verificar se o diretório foi corretamente exportado:
   ```bash
   sudo exportfs -v
   ```


---

### 6.2 Configurar o Cliente NFS na Máquina WEB

1. **Atualizar o sistema**  
   Assim como no servidor, é importante atualizar o sistema do cliente NFS:
   ```bash
   sudo apt update
   ```

2. **Instalar o NFS Common**  
   Instale o pacote necessário para montar os compartilhamentos NFS:
   ```bash
   sudo apt install nfs-common -y
   ```

3. **Criar o diretório de montagem**  
   Crie o diretório onde o compartilhamento NFS será montado:
   ```bash
   sudo mkdir -p /srv
   ```

4. **Montar o compartilhamento NFS**  
   Monte o diretório compartilhado do servidor NFS no diretório de montagem local:
   ```bash
   sudo mount 192.168.100.4:/srv/web /srv
   ```

5. **Verificar a montagem**  
   Verifique se o compartilhamento foi montado corretamente, utilizando o comando `df -h`:
   ```bash
   df -h
   ```

7. **Adicionar ao fstab para montagem automática**  
   Para que o compartilhamento NFS seja montado automaticamente ao iniciar o sistema, edite o arquivo `/etc/fstab`:
   ```bash
   sudo nano /etc/fstab
   ```

   Adicione a seguinte linha ao final do arquivo:
   ```txt
   192.168.100.4:/srv/web /srv nfs defaults 0 0
   ```

8. **Testar a montagem automática**  
   Após editar o `fstab`, faça um teste reiniciando a máquina e verificando se o compartilhamento foi montado automaticamente:
   ```bash
   sudo reboot
   df -h
   ```

**Criar snapshot da máquina UBUNTU e WEB**

---

Aqui está a versão melhorada e complementada do seu texto:

---

## 7. Configurar o PROXY

## 7.1 Configurar o PROXY na máquina DNS1

### 1. **Instalar o Squid (Proxy Server)**
   Para instalar o Squid, um dos servidores proxy mais populares, execute o seguinte comando:
   ```bash
   sudo apt update && sudo apt install squid -y
   ```

### 2. **Acessar o diretório de configuração do Squid**
   O arquivo de configuração do Squid está localizado no diretório `/etc/squid`. Acesse o diretório com o comando:
   ```bash
   cd /etc/squid
   ```

### 3. **Criar um backup do arquivo de configuração original**
   Antes de fazer qualquer alteração no arquivo de configuração, é recomendado criar um backup do arquivo original para garantir que você possa restaurá-lo em caso de problemas:
   ```bash
   sudo cp squid.conf squid.conf.backup
   ```

### 4. **Limpar e formatar o arquivo de configuração**
   O arquivo de configuração do Squid pode conter comentários e linhas em branco que não são necessários. Use o comando `sed` para limpar o arquivo, removendo:
   - Comentários (linhas que começam com `#`).
   - Linhas em branco.
   - Múltiplas quebras de linha consecutivas, que serão substituídas por apenas uma.
   
   Para fazer isso, execute:
   ```bash
   sudo sed -i '/^\s*#/d; /^\s*$/d' squid.conf
   ```

### 5. **Editar o arquivo de configuração do Squid**
   Agora, edite o arquivo `squid.conf` para configurar o proxy conforme necessário. Use o seguinte comando para abrir o arquivo em um editor de texto:
   ```bash
   sudo nano squid.conf
   ```

   **ATENÇÃO:** O Squid segue uma ordem de prioridade nas regras. Aqui está uma sequência recomendada para a organização das regras:

#### 5.1. **Definir Permissões Explícitas**
   Primeiramente, defina regras que permitam acessos específicos, que devem ter prioridade sobre as outras configurações.
   
   Exemplo:
   ```bash
   acl usuarios src 192.168.0.0/24  # Definindo a rede de usuários permitidos
   http_access allow usuarios
   http_access deny all
   ```

  **OBSERVAÇÃO: O COMANDO `http_access allow usuarios`, DEVE FICAR ANTES DO COMANDO `http_access deny all`**

**PARA TESTAR CONFIGURE O FIREWALL NO FIREFOX DA MÁQUINA UBUNTU**

---

# 7.2 Configuração do PROXY na Máquina Ubuntu

### 1. **Configurar Proxy no Navegador Firefox**

1. **Abrir o Firefox**:
   - Acesse as configurações do navegador através de **Configurações** > **Rede** > **Configurar Rede**.

2. **Escolher Configuração Manual de Proxy**:
   - Selecione a opção **Configuração manual de proxy**.

3. **Inserir os Dados do Proxy**:
   - **Endereço do Proxy**: Insira o IP do DNS1 (`192.168.100.2`).
   - **Porta**: Insira a porta do Squid (geralmente, `3128`).

4. **Configuração para HTTPS**:
   - Marque a opção **Usar também para HTTPS** para garantir que o proxy seja utilizado também para conexões HTTPS.

5. **Salvar Configurações**:
   - Após inserir os dados corretamente, clique em **OK** ou **Salvar** para aplicar as configurações de proxy.

---

Aqui está um passo a passo detalhado para configurar uma instância do Moodle em um servidor Ubuntu que já possui Apache e PHPMyAdmin instalados:

---

### **Passo 1: Verifique os requisitos do Moodle**
Antes de começar, confirme que seu servidor atende aos requisitos de sistema do Moodle:
- **PHP:** Verifique a versão necessária para o Moodle que você está instalando.
- **MySQL/MariaDB ou PostgreSQL:** O Moodle requer um banco de dados suportado.
- **Extensões PHP:** Moodle exige várias extensões PHP como `gd`, `intl`, `mysqli`, `soap`, entre outras.

---

### **Passo 2: Atualize o sistema**
Certifique-se de que o sistema está atualizado:
```bash
sudo apt update
```

---

### **Passo 3: Instale dependências necessárias**
Instale os pacotes essenciais para o Moodle:
```bash
sudo apt install apache2 mysql-server php libapache2-mod-php php-mysql php-xml php-mbstring php-curl php-zip php-intl php-soap php-gd php-xmlrpc unzip -y
```

Reinicie o Apache para carregar as extensões PHP:
```bash
sudo systemctl restart apache2
```

---

### **Passo 4: Baixe o Moodle**
Baixe a versão mais recente do Moodle diretamente do site oficial:
```bash
wget https://download.moodle.org/download.php/stable405/moodle-latest-405.tgz
```

Extraia o pacote e mova os arquivos para o diretório do servidor web:
```bash
tar -xvzf moodle-latest-405.tgz
sudo mv moodle /srv/prova/ava/
```

---

### **Passo 5: Configure o diretório de dados**
O Moodle precisa de um diretório para armazenar dados, que não deve estar acessível publicamente. Crie-o fora do diretório raiz do Apache:
```bash
sudo mkdir /var/moodledata
sudo chown -R www-data:www-data /var/moodledata
sudo chmod -R 770 /var/moodledata
```

---

### **Passo 6: Configure permissões**
Certifique-se de que o diretório do Moodle no Apache também tenha permissões apropriadas:
```bash
sudo chown -R www-data:www-data /srv/prova/ava/moodle
sudo chmod -R 755 /srv/prova/ava/moodle
```

---

### **Passo 7: Configure o banco de dados**
1. Acesse o MySQL:
```bash
sudo mysql -u root -p
```
2. Crie um banco de dados e um usuário:
```sql
CREATE DATABASE moodle DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER 'moodleuser'@'localhost' IDENTIFIED BY 'Ifro@2025';
GRANT ALL PRIVILEGES ON moodle.* TO 'moodleuser'@'localhost';
FLUSH PRIVILEGES;
EXIT;
```

---

### **Passo 8: Configure o Apache para o Moodle**
Crie um arquivo de configuração para o Moodle:
```bash
sudo nano /etc/apache2/sites-available/moodle.conf
```

Adicione o seguinte conteúdo:
```apache
<VirtualHost *:443>
    ServerAdmin admin@seusite.com
    DocumentRoot /srv/prova/ava/moodle
    ServerName ava.prova.lan

    <Directory /srv/prova/ava/moodle>
        Options FollowSymlinks
        AllowOverride All
        Require all granted
    </Directory>

    ErrorLog ${APACHE_LOG_DIR}/moodle_error.log
    CustomLog ${APACHE_LOG_DIR}/moodle_access.log combined
</VirtualHost>
```

Ative a configuração e os módulos necessários:
```bash
sudo a2ensite moodle
sudo a2enmod rewrite
sudo systemctl reload apache2
```

---

### **Passo 9: Finalize a instalação**
1. Acesse o Moodle no navegador: `http://seu-ip-ou-dominio/moodle`.
2. Siga as instruções da página para completar a instalação:
   - Escolha o banco de dados MySQL e forneça as credenciais configuradas no **Passo 7**.
   - Configure o administrador com o nome de usuário padrão e a senha: `Ifro@2025`.

---

### **Passo 10: Teste a instalação**
Acesse o Moodle e verifique se está funcionando corretamente. Você pode criar cursos e usuários adicionais para validar a funcionalidade.

Se precisar de mais assistência, estou à disposição! 😊
