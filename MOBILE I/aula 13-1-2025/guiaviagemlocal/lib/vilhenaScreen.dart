import 'package:flutter/material.dart';

class VilhenaScreen extends StatefulWidget {
  const VilhenaScreen({super.key});

  @override
  State<VilhenaScreen> createState() => _VilhenaScreenState();
}

class _VilhenaScreenState extends State<VilhenaScreen> {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text("VilhenaScreen"),
        centerTitle: true,
        backgroundColor: Colors.blue,
        foregroundColor: Colors.white,
      ),
    );
  }
}
