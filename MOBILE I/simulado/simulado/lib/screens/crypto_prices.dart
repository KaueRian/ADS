import 'package:flutter/material.dart';
import 'package:simulado/widgets/colors.dart';

class CryptoPrices extends StatefulWidget {
  const CryptoPrices({super.key});

  @override
  State<CryptoPrices> createState() => _CryptoPricesState();
}

class _CryptoPricesState extends State<CryptoPrices> {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('Crypto Prices'),
        centerTitle: true,
        backgroundColor: Cores.backgroundColor,
        foregroundColor: Cores.foregroundColor,
      ),
    );
  }
}
