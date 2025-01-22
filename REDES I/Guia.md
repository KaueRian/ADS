## Pré-requisitos e Observações Gerais
- **Adaptador Host-Only**: Configure a placa de rede VirtualBox `Host-Only Ethernet Adapter` com o IP `192.168.56.1/24` e **desative o servidor DHCP**.
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

### **Configurações do VirtualBox**
1. **Configuração do Host-Only Ethernet Adapter:**
   - IP fixo: `192.168.56.1/24`
   - Desative o DHCP.

2. **Criar as 5 VMs:**
   - Criar o Gateway (Debian CLI).
   - Configurar a primeira placa de rede como primária, com DHCP ativo.
   - Defina o domínio como `lab.lan` (ou conforme o professor informar).

3. **Configuração de Rede:**
   - **Adaptador 1:** Modo NAT.
   - **Adaptador 2:** Modo Host-Only, nome: `VirtualBox Host-Only Ethernet Adapter`.
   - **Adaptador 3:** Modo Rede Interna, nome: `SRC1`.

4. **Configuração de IP em `/etc/network/interfaces`:**
   ```bash
   allow-hotplug enp0s8
   iface enp0s8 inet static
   address 172.16.100.1/24

   allow-hotplug enp0s9
   iface enp0s9 inet static
   address 192.168.56.2/24
   ```

5. **Instalar `sudo`:**
   - `apt update && apt install sudo`
   - Edite o grupo com: `nano /etc/group`
   - Clique em: `Alt + shift + 3`
   - Altere a linha 21 para: `sudo:x:27:aluno`
   - Salve e saia.

6. **Desligar a máquina:**
   ```bash
   /sbin/shutdown -h now
   ```

7. **Ligar a máquina em modo headless e acessar via SSH:**
   - Acesse via SSH: `ssh aluno@192.168.56.2`.

---

### **Configuração do Firewall e Acesso via SSH**
1. **Atualize o sistema:**
   ```bash
   sudo apt update && sudo apt upgrade -y
   ```

2. **Configuração do DNS:**
   - Edite o arquivo `/etc/dhcp/dhclient.conf` e adicione:
   ```bash
   supersede domain-name-servers 172.16.100.2, 172.16.100.3, 8.8.8.8;
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

     - Organize os repositorios:
     ```bash
     sudo nano /etc/apt/souces.list
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

### **Configuração do DHCP**
1. **Acesse via SSH:**
   ```bash
   ssh -p 51000 aluno@192.168.56.2
   ```

2. **Instalar e configurar o servidor DHCP:**
   ```bash
   sudo apt update && sudo apt install isc-dhcp-server -y
   ```

3. **Configurar o arquivo `/etc/default/isc-dhcp-server`:**
   ```bash
   INTERFACESv4="enp0s8"
   ```

4. **Configuração do arquivo `/etc/dhcp/dhcpd.conf`:**
   Adicione a configuração de rede:
   ```bash
   subnet 172.16.100.0 netmask 255.255.255.0 {
     range 172.16.100.50 172.16.100.250;
     option domain-name-servers 8.8.8.8, 172.16.100.2, 172.16.100.3;
     option domain-name "lab.lan";
     option routers 172.16.100.1;
     option broadcast-address 172.16.100.255;
     default-lease-time 600;
     max-lease-time 7200;
   }
   ```

---

### **Configuração do Ubuntu**
1. **Adaptador 1:** Rede Interna `intnet`.
2. **Configuração de IP via DHCP:**
   - Edite o arquivo `/etc/systemd/resolved.conf`:
   ```bash
   [Resolve]
   DNS=172.16.100.2 172.16.100.3 8.8.8.8
   Domains=lab.lan
   ```

3. **Remova a configuração existente:**
   ```bash
   sudo rm /etc/resolved.conf
   ```

4. **Reinicie a máquina:**
   ```bash
   sudo reboot
   ```

5. **Teste a conexão com a internet e o ping para o domínio `lab.lan`.**

6. **Desligue a máquina e crie o Snapshot.**

---

### **Configuração do DNS1 (Servidor DNS)**
1. **Ubuntu Server CLI:**
   - **Adaptador 1:** Rede Interna (mesma do gateway).
   - **Configuração de IP fixo:**
     Edite o arquivo `/etc/netplan/50-cloud-init.yaml`:
     ```yaml
     network:
       version: 2
       ethernets:
         enp0s3:
           dhcp4: false
           addresses:
             - 172.16.100.2/24
           nameservers:
             addresses:
               - 8.8.8.8
             search:
               - lab.lan
           routes:
             - to: default
               via: 172.16.100.1
     ```
   - Aplique a configuração:
   ```bash
   sudo netplan apply
   ```

2. **Instale e configure o BIND9 (DNS):**
   ```bash
   sudo apt install bind9
   ```

3. **Configure os arquivos do BIND9:**
   Edite `/etc/bind/named.conf.default-zones` para adicionar as zonas:
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

4. **Criação e configuração das zonas e arquivos de DNS:**
   - Crie o diretório `ifro` e copie os arquivos necessários.
   - Edite os arquivos `lab.db` e `lab.rev` conforme as instruções fornecidas.

5. **Verifique a configuração do BIND9:**
   ```bash
   sudo named-checkconf
   sudo named-checkzone laboratorio.lan ifro/lab.db
   sudo named-checkzone 100.16.172.in-addr.arp ifro/lab.rev
   ```

6. **Reinicie o serviço do BIND9:**
   ```bash
   sudo systemctl restart bind9
   sudo systemctl status bind9
   ```

7. **Teste o DNS com o comando `ping lab.lan`.**

---

### **Configuração do DNS2**

1. **Criar Clone Linkado:**
   - Gere novos endereços MAC para todas as placas de rede.
   - Acesse a máquina via VirtualBox (não via SSH).
   
2. **Definir o Hostname:**
   ```bash
   sudo hostnamectl set-hostname dns2
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
           - 172.16.100.3/24
         nameservers:
           addresses:
             - 8.8.8.8
           search:
             - lab.lan
         routes:
           - to: default
             via: 172.16.100.1
   ```

4. **Reiniciar e Verificar Conexão:**
   - Reinicie a máquina:
   ```bash
   sudo reboot
   ```
   - Teste o IP, ping para `lab.lan` e o gateway.
   - Desligue a máquina e crie um snapshot.

---

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
           - 172.16.100.3/24
         nameservers:
           addresses:
             - 8.8.8.8
           search:
             - lab.lan
         routes:
           - to: default
             via: 172.16.100.1
   ```

2. **Configuração de DNS:**
   - Edite `/etc/systemd/resolved.conf`:
   ```ini
   [Resolve]
   DNS=172.16.100.2 172.16.100.3 8.8.8.8
   Domains=lab.lan
   ```
   - Reinicie a máquina e verifique o IP, teste internet com `ping lab.lan` e `ping` para o gateway.

3. **Configuração do Apache:**
   - Instale e configure o Apache:
   ```bash
   sudo apt update && sudo apt upgrade -y
   sudo apt install apache2 -y
   sudo a2enmod ssl
   sudo a2enmod rewrite
   sudo systemctl restart apache2
   sudo apt install php -y
   ```
   - Crie o arquivo `/var/www/html/index.php`:
   ```php
   <?php phpinfo(); ?>
   ```

4. **Configuração de VirtualHost:**
   - Edite `/etc/apache2/sites-available/web.lab.conf`:
   ```apache
   <VirtualHost *:80>
   ServerAdmin meuemail@email.com
   ServerName lab.lan
   ServerAlias web.lab.lan
   DocumentRoot /srv/lab/web
   ErrorLog ${APACHE_LOG_DIR}/web_error.log
   CustomLog ${APACHE_LOG_DIR}/web_access.log combined
   </VirtualHost>
   ```
   - Crie a pasta `/srv/lab/web` e edite `index.php`:
   ```php
   <?php
   echo getcwd() . "\n";
   chdir('cvs');
   ?>
   ```

5. **Configuração SSL/HTTPS:**
   - Instale e configure SSL:
   ```bash
   sudo apt install openssl ssl-cert
   sudo mkdir -p /etc/apache2/ssl
   openssl genrsa -out /etc/apache2/ssl/web.key 2048
   openssl req -new -key /etc/apache2/ssl/web.key -out /etc/apache2/ssl/web.csr
   openssl x509 -req -days 365 -in /etc/apache2/ssl/web.csr -signkey /etc/apache2/ssl/web.key -out /etc/apache2/ssl/web.crt
   sudo chmod 600 /etc/apache2/ssl/web.key
   sudo chmod 600 /etc/apache2/ssl/web.csr
   ```

6. **Configuração VirtualHost SSL:**
   - Edite `/etc/apache2/sites-available/web-ssl.conf`:
   ```apache
   <VirtualHost *:443>
   ServerAdmin suporte@laboratorio.lan
   ServerName web.lab.lan:443
   DocumentRoot /srv/lab/web
   ErrorLog ${APACHE_LOG_DIR}/web-error.log
   CustomLog ${APACHE_LOG_DIR}/web.log combined

   SSLEngine on
   SSLCertificateFile /etc/apache2/ssl/web.crt
   SSLCertificateKeyFile /etc/apache2/ssl/web.key
   </VirtualHost>

   <VirtualHost *:80>
   RewriteEngine on
   ServerName web.lab.lan
   Options FollowSymLinks
   RewriteCond %{SERVER_PORT} 80
   RewriteRule ^(.*)$ https://web.lab.lan/ [R,L]
   </VirtualHost>
   ```
   - Ative o site e reinicie o Apache:
   ```bash
   sudo a2ensite web-ssl.conf
   sudo systemctl restart apache2
   ```

---

### **Configuração do FTP**

1. **Configurações no DNS1:**
   - Edite `/etc/bind/lab/lab.db`:
   ```bash
   @       IN      A       172.16.100.2
   ns      IN      A       172.16.100.2
   web     IN      A       172.16.100.4
   ftp     IN      A       172.16.100.4
   ```
   - Reinicie o Bind9:
   ```bash
   sudo systemctl restart bind9
   ```

2. **Configurações na Máquina WEB:**
   - Instale e configure o ProFTPD:
   ```bash
   sudo apt install proftpd
   sudo mkdir -p /srv/lab/ftp
   sudo chown aluno:aluno /srv/lab/ftp
   sudo chmod 755 /srv/lab/ftp
   sudo nano /etc/proftpd/proftpd.conf
   ServerName "LAB"
   DefaultRoot /srv/lab/ftp
   sudo systemctl restart proftpd
   ```

3. **Teste FTP no Ubuntu:**
   ```bash
   ftp ftp.lab.lan
   ```

---

### **Configuração do NFS**

1. **Configuração do Servidor NFS na Máquina WEB:**
   ```bash
   sudo apt install nfs-kernel-server -y
   sudo mkdir -p /srv/lab/docs
   sudo chown nobody:nogroup /srv/lab/docs
   sudo chmod 755 /srv/lab/docs
   sudo nano /etc/exports
   /srv/lab/docs 172.16.100.0/24(rw,no_root_squash,sync)
   sudo systemctl restart nfs-kernel-server
   sudo exportfs -v
   ```

2. **Configuração do Cliente NFS (Ubuntu):**
   ```bash
   sudo apt install nfs-common -y
   sudo mkdir -p /nfs/docs
   sudo mount 172.16.100.4:/srv/lab/docs /nfs/docs
   df -h
   ```

3. **Configuração de Montagem Automática:**
   - Edite `/etc/fstab`:
   ```bash
   172.16.100.4:/srv/lab/docs /nfs/docs nfs defaults 0 0
   ```

---

### **Configuração do Proxy**

1. **Configuração do Proxy no Gateway:**
   ```bash
   sudo apt install squid
   sudo cp /etc/squid/squid.conf /etc/squid/squid.conf.original
   sudo nano /etc/squid/squid.conf
   # Adicione:
   1342 # rede interna
   1343 acl aula src 172.16.100.0/24
   1552 #permitindo rede internta
   1553 http_access allow aula
   ```

2. **Configuração do Proxy no Ubuntu (Firefox):**
   - Vá para **Configurações > Rede > Configurar Rede**.
   - Escolha **Configuração manual de proxy**.
   - Insira:
     - **Endereço do Proxy:** 172.16.100.1
     - **Porta:** A porta definida no Squid (ex: 3128).
   - Marque a opção **Usar também para HTTPS**.

3. **Teste:**
   - Salve as configurações e teste o proxy.

---

### **Finalização**

- Após concluir as configurações, crie snapshots para todas as máquinas configuradas.
