import 'package:flutter/material.dart';

class Home2 extends StatelessWidget {
  const Home2({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('Parabéns'),
        centerTitle: true,
        foregroundColor: Colors.white,
        backgroundColor: Colors.blue,
      ),
      body: Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            Text(
              'Parabéns você acertou',
              style: TextStyle(fontSize: 32, color: Colors.black),
            ),
            SizedBox(
              height: 32,
            ),
            ElevatedButton(
                style: TextButton.styleFrom(
                    foregroundColor: Colors.white, backgroundColor: Colors.red),
                onPressed: () {
                  Navigator.pop(context);
                },
                child: Text('Voltar')),
            SizedBox(
              height: 32,
            ),
          ],
        ),
      ),
    );
  }
}
