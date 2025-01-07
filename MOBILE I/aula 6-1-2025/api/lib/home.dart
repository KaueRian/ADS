import 'package:flutter/material.dart';
import 'package:dio/dio.dart';

class Home extends StatefulWidget {
  const Home({super.key});

  @override
  State<Home> createState() => _HomeState();
}

class _HomeState extends State<Home> {
  final dio = Dio();

  Future<Map<String, dynamic>> getHttp() async {
    final response = await dio.get('https://dog.ceo/api/breeds/image/random');
    print(response);
    return response.data;
  }

  Map<String, dynamic> resposta = {};

  var http =
      'https://images.dog.ceo/breeds/bullterrier-staffordshire/n02093256_7830.jpg';

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('Cachorros tops'),
        centerTitle: true,
        backgroundColor: Colors.blue,
        foregroundColor: Colors.white,
      ),
      body: Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            Text('Clique no botão para sortear um cachorro:'),
            SizedBox(
              height: 32,
            ),
            Container(
              padding: EdgeInsets.all(32),
              width: 350,
              height: 350,
              //color: Colors.red,
              child: Image.network(http),
            ),
            SizedBox(
              height: 32,
            ),
            ElevatedButton(
                onPressed: () async {
                  resposta = await getHttp();
                  setState(() {
                    for (var entry in resposta.entries) {
                      print(entry.key + entry.value);
                      http = entry.value;
                      print(http);
                      break;
                    }
                  });
                },
                child: Text('Sortear imagem de cachorro')),
          ],
        ),
      ),
    );
  }
}
