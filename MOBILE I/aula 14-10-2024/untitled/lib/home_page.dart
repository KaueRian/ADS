import 'package:flutter/material.dart';

class HomePage extends StatefulWidget {
  const HomePage({super.key});

  @override
  State<HomePage> createState() => _HomePageState();
}

class _HomePageState extends State<HomePage> {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        foregroundColor: Colors.white70,
        title: const Text(
          'Meu app!',
          style: TextStyle(fontSize: 20),
        ),
        backgroundColor: Colors.orangeAccent,
      ),
      body: const Column(
        children: [
          Text('Primeiro texto.'),
          Text('Segundo texto.'),
          Text('Terceiro texto.')
        ],
      ),
    );
  }
}
