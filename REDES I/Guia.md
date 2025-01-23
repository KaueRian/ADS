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
   - Defina o domínio como `laboratorio.lan` (ou conforme o professor informar).

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
     sudo nano /etc/apt/sources.list
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
     option domain-name "laboratorio.lan";
     option routers 172.16.100.1;
     option broadcast-address 172.16.100.255;
     default-lease-time 600;
     max-lease-time 7200;
   }
   ```

---

### **Configuração do Ubuntu**
1. **Adaptador 1:** Rede Interna `intnet`.

  - Instale o ubuntu normalmente sem internet.

2. **Configuração de IP via DHCP:**
   - Edite o arquivo `/etc/systemd/resolved.conf`:
   ```bash
   [Resolve]
   DNS=172.16.100.2 172.16.100.3 8.8.8.8
   Domains=laboratorio.lan
   ```

3. **Remova a configuração existente:**
   ```bash
   sudo rm /etc/resolved.conf
   ```

4. **Reinicie a máquina:**
   ```bash
   sudo reboot
   ```
**Desligue e ligue novamente a placa de rede**

5. **Teste a conexão com a internet e o ping para o domínio `laboratorio.lan`.**

6. **Desligue a máquina e crie o Snapshot da máquina Gateway e Ubuntu.**

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
               - laboratorio.lan
           routes:
             - to: default
               via: 172.16.100.1
     ```
   - Aplique a configuração:
   ```bash
   sudo netplan apply
   ```

   - Teste acesso via ssh:
   ```bash
   ssh -p 51000 aluno@192.168.56.2
   ```

   **Se funcionar faça Snapshot da configuração de rede concluída**

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
           allow-transfer { 172.16.100.3; };
   };

   zone "100.16.172.in-addr.arpa" {
           type master;
           file "/etc/bind/ifro/lab.rev";
           allow-transfer { 172.16.100.3; };
   };
   ```

4. **Criação e configuração das zonas e arquivos de DNS:**
   - Crie o diretório `ifro` e copie os arquivos necessários.
   ```bash
   cd /etc/bind
   ```
   ```bash
   mkdir ifro
   ```
   ```bash
   sudo cp db.local ifro/lab.db
   ```
   ```bash
   sudo cp db.127 ifro/lab.rev
   ```
   - Edite os arquivos `lab.db` e `lab.rev` conforme as instruções fornecidas.

   ```bash
   sudo nano lab.db
   ```

   ```bash
   ;
   ; BIND data file for local loopback interface
   ;
   $TTL    604800
   @       IN      SOA     laboratorio.lan. root.laboratorio.lan. (
                   1         ; Serial
                   604800    ; Refresh
                   86400     ; Retry
                   2419200   ; Expire
                   604800 )  ; Negative Cache TTL
   ;
   @       IN      NS      laboratorio.lan.
   @       IN      A       172.16.100.2
   ns      IN      A       172.16.100.2
   web     IN      A       172.16.100.4
   www     IN      CNAME   web.laboratorio.lan.
   dns1    IN      CNAME   ns.laboratorio.lan.
   ```

   ```bash
   sudo nano lab.rev
   ```

   ```bash
   ;
   ; BIND reverse data file for local loopback interface
   ;
   $TTL    604800
   @       IN      SOA     laboratorio.lan. root.laboratorio.lan. (
                   1         ; Serial
                   604800    ; Refresh
                   86400     ; Retry
                   2419200   ; Expire
                   604800 )  ; Negative Cache TTL
   ;
   @       IN      NS      laboratorio.lan.
   2       IN      PTR     laboratorio.lan.
   4       IN      PTR     web.laboratorio.lan.
   ```
  
5. **Verifique a configuração do BIND9:**
   ```bash
   sudo named-checkconf
   sudo named-checkzone laboratorio.lan lab.db
   sudo named-checkzone 100.16.172.in-addr.arp lab.rev
   ```

**Defina o DNS:**

```bash
sudo nano /etc/systemd/resolved.conf
```
```bash
[Resolve]
DNS=172.16.100.2 172.16.100.3 8.8.8.8
Domains=laboratorio.lan
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

8. **Teste o DNS com o comando `ping laboratorio.lan`.**

**Salve o SNAPSHOT do DNS**

---

### **Configuração do DNS2**

1. **Criar Clone Linkado:**
   - Gere novos endereços MAC para todas as placas de rede.
   - Acesse a máquina via VirtualBox (não via SSH).
   
2. **Definir o Hostname:**
   ```bash
   sudo hostnamectl set-hostname dns2
   ```

**Definir o /etc/hosts:**
   ```bash
   sudo nano /etc/hosts
   ```
   ```bash
   127.0.0.1 localhost
   127.0.1.1 dns2
   172.16.100.3    dns2    dns2.laboratorio.lan
   172.16.100.2    dns1    dns1.laboratorio.lan
   172.16.100.1    gateway gateway.laboratorio.lan

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
           - 172.16.100.3/24
         nameservers:
           addresses:
             - 8.8.8.8
           search:
             - laboratorio.lan
         routes:
           - to: default
             via: 172.16.100.1
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
   DNS=172.16.100.2 8.8.8.8
   Domains=laboratorio.lan
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
   - Teste o IP, ping para `laboratorio.lan` e o gateway.
   - Desligue a máquina e crie um snapshot.

### Configuração do DNS2 como Slave no Bind9

#### **Passo 1: Instalar o Bind9 no DNS2**
1. Atualize o sistema:
   ```bash
   sudo apt update
   ```
2. Instale o Bind9:
   ```bash
   sudo apt install bind9
   ```

---

#### **Passo 2: Configurar as Zonas no DNS2**
1. Edite o arquivo de zonas padrão do Bind:
   ```bash
   sudo nano /etc/bind/named.conf.default-zones
   ```
2. Adicione as configurações abaixo para criar as zonas **laboratorio.lan** e a zona reversa **100.16.172.in-addr.arpa**:
   ```bash
   // Zona direta para laboratorio.lan
   zone "laboratorio.lan" {
       type slave;
       file "/etc/bind/ifro/lab.db"; // Caminho do arquivo de zona
       masters { 172.16.100.2; };    // IP do servidor master
   };

   // Zona reversa para 172.16.100.0/24
   zone "100.16.172.in-addr.arpa" {
       type slave;
       file "/etc/bind/ifro/lab.rev"; // Caminho do arquivo de zona reversa
       masters { 172.16.100.2; };     // IP do servidor master
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
   dig @172.16.100.3 laboratorio.lan
   dig @172.16.100.3 -x 172.16.100.2
   ```

2. Se tudo estiver configurado corretamente, você verá as respostas das consultas apontando para o DNS1 como servidor mestre.

---

- Use o comando abaixo para identificar problemas:
  ```bash
  sudo named-checkconf
  ```
- Para validar arquivos de zona:
  ```bash
  sudo named-checkzone laboratorio.lan /etc/bind/ifro/lab.db
  sudo named-checkzone 100.16.172.in-addr.arpa /etc/bind/ifro/lab.rev
  ```

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
           - 172.16.100.4/24
         nameservers:
           addresses:
             - 8.8.8.8
           search:
             - laboratorio.lan
         routes:
           - to: default
             via: 172.16.100.1
   ```

   - Aplique a configuração:
   ```bash
   sudo netplan apply
   ```

2. **Configuração de DNS:**
   - Edite `/etc/systemd/resolved.conf`:
   ```ini
   [Resolve]
   DNS=172.16.100.2 172.16.100.3 8.8.8.8
   Domains=laboratorio.lan
   ```
   ```bash
   sudo rm /etc/resolv.conf
   ```
   - Reinicie a máquina e verifique o IP, teste internet com `ping laboratorio.lan` e `ping` para o gateway.
   - Desligue a máquina e crie um snapshot.

3. **Configuração do Apache:**
   - Instale e configure o Apache:
   ```bash
   sudo apt update
   ```
   ```bash
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
   ServerName laboratorio.lan
   ServerAlias web.laboratorio.lan
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
   ServerName web.laboratorio.lan:443
   DocumentRoot /srv/lab/web
   ErrorLog ${APACHE_LOG_DIR}/web-error.log
   CustomLog ${APACHE_LOG_DIR}/web.log combined

   SSLEngine on
   SSLCertificateFile /etc/apache2/ssl/web.crt
   SSLCertificateKeyFile /etc/apache2/ssl/web.key
   </VirtualHost>

   <VirtualHost *:80>
   RewriteEngine on
   ServerName web.laboratorio.lan
   Options FollowSymLinks
   RewriteCond %{SERVER_PORT} 80
   RewriteRule ^(.*)$ https://web.laboratorio.lan/ [R,L]
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
   ftp ftp.laboratorio.lan
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
