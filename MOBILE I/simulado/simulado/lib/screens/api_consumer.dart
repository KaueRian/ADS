import 'package:flutter/material.dart';
import 'package:simulado/widgets/colors.dart';

class ApiConsumer extends StatefulWidget {
  const ApiConsumer({super.key});

  @override
  State<ApiConsumer> createState() => _ApiConsumerState();
}

class _ApiConsumerState extends State<ApiConsumer> {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('Api Consumer'),
        centerTitle: true,
        backgroundColor: Cores.backgroundColor,
        foregroundColor: Cores.foregroundColor,
      ),
    );
  }
}
