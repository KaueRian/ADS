import 'package:flutter/material.dart';
import 'package:url_launcher/url_launcher.dart';

Uri _parqueCircuito = Uri.parse(
    'https://sema.portovelho.ro.gov.br/artigo/33602/parque-circuito-recebe-cerca-de-dois-mil-visitantes-diariamente-para-atividade-fisica-e-lazer');

Future<void> _launchUrlParqueCircuito() async {
  if (!await launchUrl(_parqueCircuito)) {
    throw Exception('Could not launch $_parqueCircuito');
  }
}

Uri _pracaTresCaixas = Uri.parse('https://rondonia.ro.gov.br/tres-caixas-dagua-e-a-praca-no-entorno-sao-simbolos-culturais-e-patrimonio-do-estado-de-rondonia/');

Future<void> _launchUrlPracaTresCaixas() async {
  if (!await launchUrl(_pracaTresCaixas)) {
    throw Exception('Could not launch $_pracaTresCaixas');
  }
}

Uri _zaniApartHotel = Uri.parse('https://www.zaniaparthotel.com.br/');

Future<void> _launchUrlZaniApartHotel() async {
  if (!await launchUrl(_zaniApartHotel)) {
    throw Exception('Could not launch $_zaniApartHotel');
  }
}

Uri _oParoca = Uri.parse('https://www.instagram.com/oparoca/');

Future<void> _launchUrloParoca() async {
  if (!await launchUrl(_oParoca)) {
    throw Exception('Could not launch $_oParoca');
  }
}

class PortoVelhoScreen extends StatefulWidget {
  const PortoVelhoScreen({super.key});

  @override
  State<PortoVelhoScreen> createState() => _PortoVelhoScreenState();
}

class _PortoVelhoScreenState extends State<PortoVelhoScreen> {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text("PortoVelhoScreen"),
        centerTitle: true,
        backgroundColor: Colors.blue,
        foregroundColor: Colors.white,
      ),
      body: Center(
          child: SingleChildScrollView(
        child: Column(
          children: [
            PontoTuristicoCard(
                imageAsset: 'assets/images/parquecircuitoportovelho.jpg',
                name: 'Parque Circuito',
                description:
                    'Rodeado por seringueiras que remetem a um importante período '
                    'de nossa história, o Parque Circuito Doutor José Adelino '
                    'é hoje uma das mais populares opções de lazer na capital.'),
            ElevatedButton(
              onPressed: _launchUrlParqueCircuito,
              child: Text('Saiba mais'),
            ),
            PontoTuristicoCard(
                imageAsset: 'assets/images/tres-caixas-d-agua-porto-velho.jpg',
                name: "Praça das Três Caixas D'Água",
                description:
                    'As Três Caixas d’Água, em Porto Velho-RO, também conhecidas '
                    'como As Três Marias, foram tombadas por sua importância '
                    'cultural para o Estado.'),
            ElevatedButton(
              onPressed: _launchUrlPracaTresCaixas,
              child: Text('Saiba mais'),
            ),
            PontoTuristicoCard(
                imageAsset: 'assets/images/zani-apart-hotel.jpg',
                name: "Zani Apart Hotel",
                description:
                    'Situado em Porto Velho, a 4 km do shopping, o ZANI APART '
                    'HOTEL oferece acomodações com Wi-Fi gratuito, '
                    'ar-condicionado e acesso a um jardim com terraço.'),
            ElevatedButton(
              onPressed: _launchUrlZaniApartHotel,
              child: Text('Saiba mais'),
            ),
            PontoTuristicoCard(
                imageAsset: 'assets/images/o-paroca-restaturante.jpg',
                name: "O Paroca Restaurante",
                description:
                    'Variedade de pratos com destaque à rabada com polenta e '
                    'agrião, bebidas e sobremesas, em atmosfera simples.'),
            ElevatedButton(
              onPressed: _launchUrloParoca,
              child: Text('Saiba mais'),
            ),
          ],
        ),
      )),
    );
  }
}

class PontoTuristicoCard extends StatelessWidget {
  final String imageAsset;
  final String name;
  final String description;

  const PontoTuristicoCard({
    super.key,
    required this.imageAsset,
    required this.name,
    required this.description,
  });

  @override
  Widget build(BuildContext context) {
    return Container(
      height: 160,
      padding: const EdgeInsets.all(16),
      child: Row(
        crossAxisAlignment: CrossAxisAlignment.center,
        children: [
          Image(image: AssetImage(imageAsset)),
          const SizedBox(width: 10),
          Expanded(
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              mainAxisAlignment: MainAxisAlignment.center,
              children: [
                Flexible(
                  child: Text(
                    name,
                    style: const TextStyle(
                      fontSize: 24,
                      color: Colors.black,
                      fontWeight: FontWeight.bold,
                    ),
                  ),
                ),
                Flexible(
                  child: Text(
                    description,
                    style: const TextStyle(
                        fontSize: 16,
                        color: Colors.black,
                        fontWeight: FontWeight.bold),
                  ),
                ),
              ],
            ),
          ),
        ],
      ),
    );
  }
}
