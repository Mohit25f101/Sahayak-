import 'dart:convert';
import 'package:flutter/material.dart';
import 'package:webview_flutter/webview_flutter.dart';
import 'package:http/http.dart' as http;

void main() {
  runApp(const MaterialApp(home: SahayakScreen()));
}

class SahayakScreen extends StatefulWidget {
  const SahayakScreen({super.key});

  @override
  State<SahayakScreen> createState() => _SahayakScreenState();
}

class _SahayakScreenState extends State<SahayakScreen> {
  late final WebViewController _controller;
  final String backendUrl = "http://10.0.2.2:8000"; // Localhost for Emulator
  // Use your PC's IP (e.g., 192.168.1.5:8000) if testing on real phone

  bool isProcessing = false;

  @override
  void initState() {
    super.initState();
    _controller = WebViewController()
      ..setJavaScriptMode(JavaScriptMode.unrestricted)
      ..loadRequest(Uri.parse('https://filesamples.com/formats/html')); 
      // ^ REPLACE THIS with your target Demo URL (e.g., a Google Form or Dummy LIC page)
  }

  // 1. Simulate Voice Command (Since actual Audio recording needs more code)
  // For the demo, you can have 3 buttons: "Fill Name", "Fill DOB", "Submit"
  // OR strictly implement Audio recording if you have time.
  Future<void> sendCommand(String textCommand) async {
    setState(() => isProcessing = true);

    try {
      // Step A: Ask Backend what to do
      final response = await http.post(
        Uri.parse('$backendUrl/analyze'),
        headers: {"Content-Type": "application/json"},
        body: jsonEncode({
          "user_command": textCommand,
          "screenshot": "base64_placeholder" // We skip screenshot upload for speed in MVP
        }),
      );

      final data = jsonDecode(response.body);
      String action = data['action'];
      String selector = data['selector'];
      String value = data['value'];
      String msg = data['voice_response'];

      ScaffoldMessenger.of(context).showSnackBar(SnackBar(content: Text(msg)));

      // Step B: Execute Logic on Website using JavaScript
      if (action == 'type') {
        _controller.runJavaScript("""
          var el = document.querySelector("$selector");
          if(el) { 
            el.value = "$value"; 
            el.style.border = "3px solid green"; // Visual Feedback
          }
        """);
      } else if (action == 'click') {
        _controller.runJavaScript("""
          var el = document.querySelector("$selector");
          if(el) { 
            el.style.border = "3px solid red"; 
            setTimeout(() => el.click(), 1000); // Wait 1s so user sees the red box
          }
        """);
      }

    } catch (e) {
      print("Error: $e");
    } finally {
      setState(() => isProcessing = false);
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text("Sahayak Browser"), backgroundColor: Colors.orange),
      body: Stack(
        children: [
          WebViewWidget(controller: _controller),
          if (isProcessing) 
            const Center(child: CircularProgressIndicator()),
        ],
      ),
      // The "Magic" Interface
      floatingActionButton: Row(
        mainAxisAlignment: MainAxisAlignment.end,
        children: [
          FloatingActionButton(
            onPressed: () => sendCommand("My name is Mohit"),
            child: const Icon(Icons.person),
          ),
          const SizedBox(width: 10),
          FloatingActionButton(
            onPressed: () => sendCommand("Submit the form"),
            backgroundColor: Colors.green,
            child: const Icon(Icons.check),
          ),
        ],
      ),
    );
  }
}