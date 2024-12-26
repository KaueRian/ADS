import 'package:flutter/material.dart';
import 'package:simulado/widgets/colors.dart';

class MotivationalPhrases extends StatefulWidget {
  const MotivationalPhrases({super.key});

  @override
  State<MotivationalPhrases> createState() => _MotivationalPhrasesState();
}

class _MotivationalPhrasesState extends State<MotivationalPhrases> {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('Motivational Phrases'),
        backgroundColor: Cores.backgroundColor,
        foregroundColor: Cores.foregroundColor,
      ),
    );
  }
}
