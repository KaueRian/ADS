import 'package:flutter/material.dart';

class Home extends StatelessWidget {
  const Home({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      home: Scaffold(
        appBar: AppBar(
          centerTitle: true,
          title: const Text("Faça seu login"),
          backgroundColor: Colors.blue,
          foregroundColor: Colors.white,
        ),
        body: Column(
          crossAxisAlignment: CrossAxisAlignment.center,
          mainAxisAlignment: MainAxisAlignment.center,
          children: <Widget>[
            const TextWidget(texto: 'E-mail', icone: Icon(Icons.email)),
            const TextWidget(texto: 'Senha', icone: Icon(Icons.lock)),
            Padding(
              padding: const EdgeInsets.all(8.0),
              child: FractionallySizedBox(
                widthFactor: 1,
                child: ElevatedButton(
                    onPressed: () {},
                    style:
                        ElevatedButton.styleFrom(backgroundColor: Colors.blue),
                    child: const Text('Entrar',
                        style: TextStyle(
                            color: Colors.white, fontWeight: FontWeight.bold))),
              ),
            ),
            const ButtonWidget(texto: "Criar uma nova conta"),
            const ButtonWidget(texto: 'Esqueci minha senha')
          ],
        ),
      ),
    );
  }
}

class TextWidget extends StatelessWidget {
  final String texto;
  final Icon icone;

  const TextWidget({
    super.key,
    required this.texto,
    required this.icone,
  });

  @override
  Widget build(BuildContext context) {
    return Padding(
      padding: const EdgeInsets.all(8),
      child: TextFormField(
        decoration: InputDecoration(
            labelText: texto, prefixIcon: icone, border: const OutlineInputBorder()),
      ),
    );
  }
}

class ButtonWidget extends StatelessWidget {
  final String texto;

  const ButtonWidget({
    super.key,
    required this.texto,
  });

  @override
  Widget build(BuildContext context) {
    return Padding(
        padding: const EdgeInsets.all(8),
        child: Text(texto,
            style: const TextStyle(color: Colors.blue, fontWeight: FontWeight.bold)));
  }
}
