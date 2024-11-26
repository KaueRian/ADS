import 'package:flutter/material.dart';

class Home1 extends StatelessWidget {
  const Home1({super.key});

  // usar listview https://api.flutter.dev/flutter/widgets/ListView-class.html

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      home: Scaffold(
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
        body: SingleChildScrollView(
          child: Expanded(
            child: Column(
              children: [
                GestureDetector(
                  onTap: () {
                    Navigator.pushNamed(
                      context,
                      '/home2',
                      arguments: CryptoCard(
                          imageUrl:
                          'https://s2.coinmarketcap.com/static/img/coins/64x64/1.png',
                          title: 'Bitcoin',
                          acronym: 'BTC',
                          price: '\$71,920.25'),
                    );
                  },
                  child: CryptoCard(
                    imageUrl:
                    "https://s2.coinmarketcap.com/static/img/coins/64x64/1.png",
                    title: "Bitcoin",
                    acronym: "BTC",
                    price: "\$71,920.25",
                  ),
                ),
                GestureDetector(
                  onTap: () {
                    Navigator.pushNamed(
                      context,
                      '/home2',
                      arguments: CryptoCard(
                        imageUrl:
                        "https://s2.coinmarketcap.com/static/img/coins/64x64/1027.png",
                        title: "Ethereum",
                        acronym: "ETH",
                        price: "\$2,667.05",
                      ),
                    );
                  },
                  child: CryptoCard(
                    imageUrl:
                    "https://s2.coinmarketcap.com/static/img/coins/64x64/1027.png",
                    title: "Ethereum",
                    acronym: "ETH",
                    price: "\$2,667.05",
                  ),
                ),
                GestureDetector(
                  onTap: () {
                    Navigator.pushNamed(
                      context,
                      '/home2',
                      arguments: CryptoCard(
                        imageUrl:
                        "https://s2.coinmarketcap.com/static/img/coins/64x64/825.png",
                        title: "Tether",
                        acronym: "USDT",
                        price: "\$1.00",
                      ),
                    );
                  },
                  child: CryptoCard(
                    imageUrl:
                    "https://s2.coinmarketcap.com/static/img/coins/64x64/825.png",
                    title: "Tether",
                    acronym: "USDT",
                    price: "\$1.00",
                  ),
                ),
                GestureDetector(
                  onTap: () {
                    Navigator.pushNamed(
                      context,
                      '/home2',
                      arguments: CryptoCard(
                          imageUrl:
                          "https://s2.coinmarketcap.com/static/img/coins/64x64/1839.png",
                          title: "BNB",
                          acronym: "BNB",
                          price: "\$604.98"),
                    );
                  },
                  child: CryptoCard(
                      imageUrl:
                      "https://s2.coinmarketcap.com/static/img/coins/64x64/1839.png",
                      title: "BNB",
                      acronym: "BNB",
                      price: "\$604.98"),
                ),
                GestureDetector(
                  onTap: () {
                    Navigator.pushNamed(
                      context,
                      '/home2',
                      arguments: CryptoCard(
                          imageUrl:
                          "https://s2.coinmarketcap.com/static/img/coins/64x64/5426.png",
                          title: "Solana",
                          acronym: "SOL",
                          price: "\$174.84"),
                    );
                  },
                  child: CryptoCard(
                      imageUrl:
                      "https://s2.coinmarketcap.com/static/img/coins/64x64/5426.png",
                      title: "Solana",
                      acronym: "SOL",
                      price: "\$174.84"),
                ),
              ],
            ),
          ),
        ),
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
                SizedBox(
                  height: 8,
                )
              ],
            ),
          ),
        ],
      ),
    );
  }
}
