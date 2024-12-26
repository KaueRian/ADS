import 'package:flutter/material.dart';
import 'screens/dashboard.dart';

void main () {
  runApp(MaterialApp(
    initialRoute: '/dashboard',
    routes: {
      '/dashboard': (context) => Dashboard(),
    },
  ));
}