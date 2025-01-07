import 'package:flutter/material.dart';
import 'package:dio/dio.dart';

class Home extends StatefulWidget {
  const Home({super.key});

  @override
  State<Home> createState() => _HomeState();
}

class _HomeState extends State<Home> {
  final dio = Dio();
  Map<String, dynamic> resposta = {}; // Store the response here
  var http = ''; // URL for the image

  // Asynchronous function to fetch data
  Future<void> getHttp() async {
    try {
      final response = await dio.get('https://dog.ceo/api/breeds/image/random');
      setState(() {
        resposta = response.data; // Update the state with the response data
        http = resposta['message']; // Assuming 'message' contains the image URL
      });
    } catch (e) {
      print('Error: $e');
    }
  }

  @override
  void initState() {
    super.initState();
    getHttp(); // Fetch data when the widget is initialized
  }

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
              child: http.isNotEmpty
                  ? Image.network(http) // Show image if URL is valid
                  : CircularProgressIndicator(), // Show a loading indicator
            ),
            SizedBox(
              height: 32,
            ),
            ElevatedButton(
                onPressed: () async {
                  await getHttp(); // Fetch new image on button press
                },
                child: Text('Sortear imagem de cachorro')),
          ],
        ),
      ),
    );
  }
}
