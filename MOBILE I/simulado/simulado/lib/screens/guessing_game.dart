import 'package:flutter/material.dart';
import 'package:simulado/widgets/colors.dart';

class GuessingGame extends StatefulWidget {
  const GuessingGame({super.key});

  @override
  State<GuessingGame> createState() => _GuessingGameState();
}

class _GuessingGameState extends State<GuessingGame> {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('Guessing Game'),
        backgroundColor: Cores.backgroundColor,
        foregroundColor: Cores.foregroundColor,
      ),
    );
  }
}
