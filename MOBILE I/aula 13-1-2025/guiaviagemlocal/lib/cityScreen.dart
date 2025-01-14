import 'package:flutter/material.dart';

class Cityscreen extends StatefulWidget {
  const Cityscreen({super.key});

  @override
  State<Cityscreen> createState() => _CityscreenState();
}

class _CityscreenState extends State<Cityscreen> {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text("CityScren"),
        centerTitle: true,
        backgroundColor: Colors.blue,
        foregroundColor: Colors.white,
      ),
    );
  }
}
