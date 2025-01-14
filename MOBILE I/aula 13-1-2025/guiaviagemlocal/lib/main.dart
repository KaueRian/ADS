import 'package:flutter/material.dart';
import 'package:guiaviajemlocal/ariquemesScreen.dart';
import 'package:guiaviajemlocal/jiParanaScreen.dart';
import 'package:guiaviajemlocal/portoVelhoScreen.dart';
import 'package:guiaviajemlocal/vilhenaScreen.dart';
import 'cityScreen.dart';
import 'home.dart';

void main() {
  runApp(MaterialApp(
    initialRoute: '/Home',
    routes: {
      '/Home': (context) => home(),
      '/CityScreen': (context) => Cityscreen(),
      '/PortoVelhoScreen': (context) => PortoVelhoScreen(),
      '/JiParanaScreen': (context) => JiParanaScreen(),
      '/AriquemesScreen': (context) => AriquemesScreen(),
      '/VilhenaScreen': (context) => VilhenaScreen(),
    },
  ));
}