import 'package:flutter/material.dart';

class JiParanaScreen extends StatefulWidget {
  const JiParanaScreen({super.key});

  @override
  State<JiParanaScreen> createState() => _JiParanaScreenState();
}

class _JiParanaScreenState extends State<JiParanaScreen> {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text("JiParanaScreen"),
        centerTitle: true,
        backgroundColor: Colors.blue,
        foregroundColor: Colors.white,
      ),
    );
  }
}
