import 'package:flutter/material.dart';

enum SampleItem { itemOne, itemTwo, itemThree, itemFour }

class home extends StatefulWidget {
  const home({super.key});

  @override
  State<home> createState() => _homeState();
}

class _homeState extends State<home> {
  SampleItem? selectedItem;

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text("Guia de viagem local"),
        centerTitle: true,
        backgroundColor: Colors.blue,
        foregroundColor: Colors.white,
      ),
      body: Center(
        child: Row(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            Text("Selecione a cidade aqui"),
            PopupMenuButton<SampleItem>(
              initialValue: selectedItem,
              onSelected: (SampleItem item) {
                setState(() {
                  selectedItem = item;
                  if (selectedItem == SampleItem.itemOne) {
                    Navigator.pushNamed(context, '/PortoVelhoScreen');
                  } else if (selectedItem == SampleItem.itemTwo) {
                    Navigator.pushNamed(context, '/JiParanaScreen');
                  } else if (selectedItem == SampleItem.itemThree) {
                    Navigator.pushNamed(context, '/AriquemesScreen');
                  } else {
                    Navigator.pushNamed(context, '/VilhenaScreen');
                  }
                });
              },
              itemBuilder: (BuildContext context) =>
                  <PopupMenuEntry<SampleItem>>[
                const PopupMenuItem<SampleItem>(
                  value: SampleItem.itemOne,
                  child: Text('Porto Velho'),
                ),
                const PopupMenuItem<SampleItem>(
                  value: SampleItem.itemTwo,
                  child: Text('Ji Paraná'),
                ),
                const PopupMenuItem<SampleItem>(
                  value: SampleItem.itemThree,
                  child: Text('Ariquemes'),
                ),
                const PopupMenuItem<SampleItem>(
                  value: SampleItem.itemFour,
                  child: Text('Vilhena'),
                ),
              ],
            ),
          ],
        ),
      ),
    );
  }
}
