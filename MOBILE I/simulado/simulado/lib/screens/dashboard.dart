import 'package:flutter/material.dart';
import 'package:simulado/widgets/colors.dart';
import 'package:simulado/models/cards.dart';

class Dashboard extends StatefulWidget {
  const Dashboard({super.key});

  @override
  State<Dashboard> createState() => _DashboardState();
}

class _DashboardState extends State<Dashboard> {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('Dashboard'),
        centerTitle: true,
        backgroundColor: Cores.backgroundColor,
        foregroundColor: Cores.foregroundColor,
      ),
      body: Column(
        mainAxisAlignment: MainAxisAlignment.center,
        children: [
          Row(
            mainAxisAlignment: MainAxisAlignment.center,
            children: [
              Cards(
                name: 'Motivational Phrases',
                description: 'Motivational Phrases',
                screen: '/motivationalPhrases',
              ),
              Cards(
                  name: 'Api Consumer',
                  description: 'Api Consumer',
                  screen: '/apiConsumer'),
            ],
          ),
          Row(
            mainAxisAlignment: MainAxisAlignment.center,
            children: [
              Cards(
                  name: 'Crypto Prices',
                  description: 'Crypto Prices',
                  screen: '/cryptoPrices'),
              Cards(
                  name: 'Guessing Game',
                  description: 'Guessing Game',
                  screen: '/guessingGame')
            ],
          )
        ],
      ),
    );
  }
}
