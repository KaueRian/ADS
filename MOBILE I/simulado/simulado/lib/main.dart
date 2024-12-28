import 'package:flutter/material.dart';
import 'screens/dashboard.dart';
import 'screens/api_consumer.dart';
import 'screens/crypto_prices.dart';
import 'screens/guessing_game.dart';
import 'screens/motivational_phrases.dart';

void main () {
  runApp(MaterialApp(
    debugShowCheckedModeBanner: false,
    initialRoute: '/dashboard',
    routes: {
      '/dashboard': (context) => Dashboard(),
      '/motivationalPhrases': (context) => MotivationalPhrases(),
      '/apiConsumer': (context) => ApiConsumer(),
      '/cryptoPrices': (context) => CryptoPrices(),
      '/guessingGame': (context) => GuessingGame(),
    },
  ));
}