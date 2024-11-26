import 'home1.dart';
import 'package:flutter/material.dart';

class Home2 extends StatelessWidget {
  const Home2({super.key});

  @override
  Widget build(BuildContext context) {
    final args = ModalRoute.of(context)!.settings.arguments as CryptoCard;

    return Scaffold(
      body: Column(
        children: [
          CryptoCard(
              imageUrl: args.imageUrl,
              title: args.title,
              acronym: args.acronym,
              price: args.price)
        ],
      ),
    );
  }
}