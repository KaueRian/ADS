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
    final response = await dio.get('https://viacep.com.br/ws/01001000/json/');
    print(response);
    return response.data;
  }

  Map<String, dynamic> respostafinal = {};

  List<String> resposta = ['Endereço: \n'];

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('Não faz isso'),
      ),
      body: Column(
        children: [
          Text('Clique'),
          ElevatedButton(
            onPressed: () async {
              respostafinal = await getHttp();
              setState(() {
                // Clear the previous response
                resposta = ['Endereço: \n'];

                // Iterate through the response and add each entry to the list
                for (var entry in respostafinal.entries) {
                  print('${entry.key}: ${entry.value}');
                  resposta.add('${entry.key}: ${entry.value}' + '\n');
                }
              });
            },
            child: Text('Clique'),
          ),
          // Use a Text widget to display the final response
          Text(resposta.join()), // Use join to display the list as a string
        ],
      ),
    );
  }
}
