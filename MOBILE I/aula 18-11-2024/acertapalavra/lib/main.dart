import 'package:flutter/material.dart';
import 'home2.dart';
import 'home3.dart';
import 'home1.dart';

void main() {
  runApp(MaterialApp(
    initialRoute: '/home1',
    routes: {
      '/home1': (context) => Home1(),
      '/home2': (context) => Home2(),
      '/home3': (context) => Home3(),
    },
  ));
}