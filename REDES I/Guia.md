Aqui está o guia revisado, com melhorias na organização, clareza e pequenas correções:

---

# Guia de Configuração de Infraestrutura de Rede

## 1. Pré-requisitos e Observações
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
     # Provides: firewall
     # Required-Start: $syslog
     # Required-Stop: $syslog
     # Default-Start: 2 3 4 5
     # Short-Description: Firewall
     ### END INIT INFO

     case $1 in
         stop)
             iptables -P OUTPUT ACCEPT
             iptables -P INPUT ACCEPT
             iptables -P FORWARD ACCEPT
             iptables -F
             iptables -t nat -F
             echo 0 > /proc/sys/net/ipv4/ip_forward
             ;;
         start)
             $0 stop
             sleep 0.5
             echo 1 > /proc/sys/net/ipv4/ip_forward
             bash ~/firewall/regras
             ;;
         restart)
             $0 start
             ;;
         *)
             echo 'Use: "stop|start|restart"'
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
     # Limpeza das regras existentes
     iptables -t nat -F
     iptables -F

     LAN=172.16.100.0/24
     LOCAL=200.50.100.0/24

     # NAT para LAN
     iptables -t nat -A POSTROUTING -s $LAN -j MASQUERADE
     
     # Exemplo de regra para SSH
     iptables -A FORWARD -p tcp -s $LOCAL -d $GATEWAY --dport 51000 -j ACCEPT
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

Este guia agora está mais estruturado e completo, pronto para implementar uma infraestrutura de rede eficiente.
