import 'package:flutter/material.dart';
import 'package:simulado/widgets/colors.dart';

class Cards extends StatelessWidget {
  final String name;
  final String description;
  final String screen;

  const Cards({
    super.key,
    required this.name,
    required this.description,
    required this.screen,
  });

  @override
  Widget build(BuildContext context) {
    return GestureDetector(
      onTap: (){
        Navigator.pushNamed(context, '${this.screen}');
      },
      child: Container(
        padding: EdgeInsets.all(16),
        color: Cores.backgroundColor,
        child: Column(
          children: [Text(this.name), Text(this.description)],
        ),
      ),
    );
  }
}
