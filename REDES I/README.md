# Guia de Configuração de Infraestrutura de Rede

## Índice
1. [Observações Iniciais](#observações-iniciais)
2. [Acesso SSH com Firewall Ativo](#acesso-ssh-com-firewall-ativo)
3. [Criação do Ambiente de Simulação Virtual](#criação-do-ambiente-de-simulação-virtual)
4. [Configuração da Máquina Gateway](#configuração-da-máquina-gateway)
5. [Configuração do Servidor DHCP](#configuração-do-servidor-dhcp)
6. [Configuração das Máquinas DNS1 e DNS2](#configuração-das-máquinas-dns1-e-dns2)
7. [Configuração do Servidor WEB](#configuração-do-servidor-web)
8. [Verificação](#verificação)

## 1. Observações Iniciais

A placa de rede **VirtualBox Host-Only Ethernet Adapter** é responsável por realizar a conexão entre a máquina virtual (VM) "Gateway" e o computador físico. Configure esta placa com:
- **IP**: `200.50.100.1/24`
- **Servidor DHCP**: desativado.

## 2. Acesso SSH com Firewall Ativo

Para acessar cada VM, utilize os comandos SSH abaixo:

```bash
# Comando para acessar cada máquina
gateway: ssh -p 51000 aluno@200.50.100.2
dns1: ssh -p 52000 aluno@200.50.100.2
dns2: ssh -p 53000 aluno@200.50.100.2
web: ssh -p 54000 aluno@200.50.100.2
