import 'package:flutter/material.dart';

class Home1 extends StatelessWidget {
  Home1({super.key});

  // Lista de dados como uma lista de mapas
  final List<Map<String, String>> lista = [
    {
      'imageUrl': 'https://s2.coinmarketcap.com/static/img/coins/64x64/1.png',
      'title': 'Bitcoin',
      'acronym': 'BTC',
      'price': '\$71,920.25',
    },
    {
      'imageUrl':
          'https://s2.coinmarketcap.com/static/img/coins/64x64/1027.png',
      'title': 'Ethereum',
      'acronym': 'ETH',
      'price': '\$2,667.05',
    },
    {
      'imageUrl': 'https://s2.coinmarketcap.com/static/img/coins/64x64/825.png',
      'title': 'Tether',
      'acronym': 'USDT',
      'price': '\$1.00',
    },
    {
      'imageUrl':
          'https://s2.coinmarketcap.com/static/img/coins/64x64/1839.png',
      'title': 'BNB',
      'acronym': 'BNB',
      'price': '\$604.98',
    },
    {
      'imageUrl':
          'https://s2.coinmarketcap.com/static/img/coins/64x64/5426.png',
      'title': 'Solana',
      'acronym': 'SOL',
      'price': '\$174.84',
    },
  ];

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        backgroundColor: Colors.orange,
        foregroundColor: Colors.white,
        title: const Text('Preços de Criptomoedas'),
        actions: [
          IconButton(
            icon: const Icon(Icons.refresh),
            onPressed: () {},
          ),
        ],
      ),
      body: ListView.builder(
        itemCount: lista.length,
        itemBuilder: (BuildContext context, int index) {
          final item = lista[index];
          return GestureDetector(
            onTap: () {
              Navigator.pushNamed(
                context,
                '/home2',
                arguments: CryptoCard(
                  imageUrl: item['imageUrl']!,
                  title: item['title']!,
                  acronym: item['acronym']!,
                  price: item['price']!,
                ),
              );
            },
            child: CryptoCard(
              imageUrl: item['imageUrl']!,
              title: item['title']!,
              acronym: item['acronym']!,
              price: item['price']!,
            ),
          );
        },
      ),
    );
  }
}

class CryptoCard extends StatelessWidget {
  final String imageUrl;
  final String title;
  final String acronym;
  final String price;

  const CryptoCard({
    super.key,
    required this.imageUrl,
    required this.title,
    required this.acronym,
    required this.price,
  });

  @override
  Widget build(BuildContext context) {
    return Container(
      height: 100,
      padding: const EdgeInsets.symmetric(horizontal: 10),
      child: Row(
        crossAxisAlignment: CrossAxisAlignment.center,
        children: [
          Image.network(
            imageUrl,
            width: 80,
          ),
          const SizedBox(width: 10),
          Expanded(
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              mainAxisAlignment: MainAxisAlignment.center,
              children: [
                Text(
                  title,
                  style: const TextStyle(
                    fontSize: 24,
                    color: Colors.black,
                    fontWeight: FontWeight.bold,
                  ),
                ),
                Text(
                  acronym,
                  style: const TextStyle(
                      fontSize: 16,
                      color: Colors.black,
                      fontWeight: FontWeight.bold),
                ),
                Text(
                  price,
                  style: const TextStyle(
                    fontSize: 24,
                    color: Colors.black,
                    fontWeight: FontWeight.bold,
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
