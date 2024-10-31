import 'package:flutter/material.dart';

class Home extends StatelessWidget {
  const Home({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      home: Scaffold(
        appBar: AppBar(
          backgroundColor: Colors.orange,
          foregroundColor: Colors.white,
          title: Text('Preços de Criptomoedas'),
          actions: [
            IconButton(
              icon: Icon(Icons.refresh),
              onPressed: () {},
            ),
          ],
        ),
        body: SingleChildScrollView(
          child: Column(
            children: [
              CryptoCard(
                imageUrl:
                    "https://s2.coinmarketcap.com/static/img/coins/64x64/1.png",
                title: "Bitcoin",
                acronym: "BTC",
                price: "\$71,920.25",
              ),
              CryptoCard(
                imageUrl:
                    "https://s2.coinmarketcap.com/static/img/coins/64x64/1027.png",
                title: "Ethereum",
                acronym: "ETH",
                price: "\$2,667.05",
              ),
              CryptoCard(
                imageUrl:
                    "https://s2.coinmarketcap.com/static/img/coins/64x64/825.png",
                title: "Tether",
                acronym: "USDT",
                price: "\$1.00",
              ),
              CryptoCard(
                  imageUrl:
                      "https://s2.coinmarketcap.com/static/img/coins/64x64/1839.png",
                  title: "BNB",
                  acronym: "BNB",
                  price: "\$604.98"),
              CryptoCard(
                  imageUrl:
                      "https://s2.coinmarketcap.com/static/img/coins/64x64/5426.png",
                  title: "Solana",
                  acronym: "SOL",
                  price: "\$174.84"),
              CryptoCard(
                  imageUrl:
                      "https://s2.coinmarketcap.com/static/img/coins/64x64/3408.png",
                  title: "USDC",
                  acronym: "USDC",
                  price: "\$1.00"),
              CryptoCard(
                  imageUrl:
                      "https://s2.coinmarketcap.com/static/img/coins/64x64/52.png",
                  title: "XRP",
                  acronym: "XRP",
                  price: "\$0.5498"),
              CryptoCard(
                  imageUrl:
                      "https://s2.coinmarketcap.com/static/img/coins/64x64/74.png",
                  title: "Dogecoin",
                  acronym: "DOGE",
                  price: "\$0.1478"),
              CryptoCard(
                  imageUrl:
                      "https://s2.coinmarketcap.com/static/img/coins/64x64/1958.png",
                  title: "TRON",
                  acronym: "TRX",
                  price: "\$0.1765"),
              CryptoCard(
                  imageUrl:
                      "https://s2.coinmarketcap.com/static/img/coins/64x64/11419.png",
                  title: "Toncoin",
                  acronym: "TON",
                  price: "\$4.88"),
              CryptoCard(
                  imageUrl:
                      "https://s2.coinmarketcap.com/static/img/coins/64x64/2010.png",
                  title: "Cardano",
                  acronym: "ADA",
                  price: "\$0.3646"),
            ],
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
      padding: EdgeInsets.symmetric(horizontal: 10),
      child: Row(
        crossAxisAlignment: CrossAxisAlignment.center,
        children: [
          Image.network(
            imageUrl,
            width: 80,
          ),
          SizedBox(width: 10),
          Expanded(
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              mainAxisAlignment: MainAxisAlignment.center,
              children: [
                Text(
                  title,
                  style: TextStyle(
                    fontSize: 24,
                    color: Colors.black,
                    fontWeight: FontWeight.bold,
                  ),
                ),
                Text(
                  acronym,
                  style: TextStyle(
                      fontSize: 16,
                      color: Colors.black,
                      fontWeight: FontWeight.bold),
                ),
              ],
            ),
          ),
          Text(
            price,
            style: TextStyle(
              fontSize: 24,
              color: Colors.black,
              fontWeight: FontWeight.bold,
            ),
          ),
        ],
      ),
    );
  }
}
