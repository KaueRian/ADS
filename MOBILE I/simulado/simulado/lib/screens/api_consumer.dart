import 'package:flutter/material.dart';
import 'package:simulado/widgets/colors.dart';
import 'package:dio/dio.dart';

class ApiConsumer extends StatefulWidget {
  const ApiConsumer({super.key});

  @override
  State<ApiConsumer> createState() => _ApiConsumerState();
}

class _ApiConsumerState extends State<ApiConsumer> {
  final dio = Dio();

  Future<Map<String, dynamic>> getHttp() async {
    final response = await dio.get('https://viacep.com.br/ws/01001000/json/');
    return response.data;
  }

  Map<String, dynamic> respostafinal = {};

  List<String> resposta = ['Endereço: \n'];

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('Api Consumer'),
        centerTitle: true,
        backgroundColor: Cores.backgroundColor,
        foregroundColor: Cores.foregroundColor,
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
                  resposta.add('${entry.key}: ${entry.value}' '\n');
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