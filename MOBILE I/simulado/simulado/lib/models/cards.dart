import 'package:flutter/material.dart';
import 'package:simulado/widgets/colors.dart';

class Cards extends StatelessWidget {
  final String name;
  final String description;

  const Cards({
    super.key,
    required this.name,
    required this.description,
  });

  @override
  Widget build(BuildContext context) {
    return Container(
      color: Cores.backgroundColor,
      child: Column(
        children: [Text(this.name), Text(this.description)],
      ),
    );
  }
}
