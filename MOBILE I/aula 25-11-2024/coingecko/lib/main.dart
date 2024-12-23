import 'package:flutter/material.dart';

import 'home1.dart';
import 'home2.dart';

void main() {
  runApp(MaterialApp(
    initialRoute: '/home1',
    routes: {
      '/home1': (context) => Home1(),
      '/home2': (context) => Home2(),
    },
  ));
}
