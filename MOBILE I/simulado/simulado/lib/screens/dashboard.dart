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
        children: [
          Cards(name: 'Motivational Phrases', description: 'Motivational Phrases')
        ],
      ),
    );
  }
}
