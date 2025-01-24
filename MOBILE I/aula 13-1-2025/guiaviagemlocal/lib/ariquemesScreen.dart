import 'package:flutter/material.dart';

class AriquemesScreen extends StatefulWidget {
  const AriquemesScreen({super.key});

  @override
  State<AriquemesScreen> createState() => _AriquemesScreenState();
}

class _AriquemesScreenState extends State<AriquemesScreen> {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text("AriquemesScreen"),
        centerTitle: true,
        backgroundColor: Colors.blue,
        foregroundColor: Colors.white,
      ),
    );
  }
}
