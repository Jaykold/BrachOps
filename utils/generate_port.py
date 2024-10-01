import random

def generate_random_port():
    return random.randint(30000, 32767)  # NodePort range

random_port = generate_random_port()
print(random_port)

'''
2. Template Your Helm Chart: Create a values.yaml file for your Helm chart:
service:
  port: {{ .Values.service.port }}

In your Kubernetes manifest template (e.g., service.yaml):
apiVersion: v1
kind: Service
metadata:
  name: my-service
spec:
  type: NodePort
  ports:
    - port: 80
      targetPort: 80
      nodePort: {{ .Values.service.port }}
  selector:
    app: my-app

3. Pass the Random Port to Helm: Run your Python script and pass the generated port to Helm:
random_port=$(python generate_port.py)
helm install my-release ./my-chart --set service.port=$random_port

Example with Kustomize
1. Generate Random Ports with Python: (Same as above)
2. Use Kustomize Generators: Create a kustomization.yaml file:
resources:
  - service.yaml

configMapGenerator:
  - name: random-port
    literals:
      - port={{random_port}}

In your service.yaml:
apiVersion: v1
kind: Service
metadata:
  name: my-service
spec:
  type: NodePort
  ports:
    - port: 80
      targetPort: 80
      nodePort: $(port)
  selector:
    app: my-app

3. Apply the Kustomization: Run your Python script and replace the placeholder in kustomization.yaml:
random_port=$(python generate_port.py)
sed -i "s/{{random_port}}/$random_port/" kustomization.yaml
kubectl apply -k .


// randomPort.ts
const availablePorts: number[] = Array.from({ length: 2768 }, (_, i) => i + 30000);

function getRandomPort(): number {
    if (availablePorts.length === 0) {
        throw new Error("No available ports left.");
    }
    const randomIndex = Math.floor(Math.random() * availablePorts.length);
    const port = availablePorts[randomIndex];
    availablePorts.splice(randomIndex, 1); // Remove the assigned port
    return port;
}

// Example usage
console.log(getRandomPort());

// Express & Socket.io
import express, { Application } from 'express';
import { createServer } from 'http';
import { Server, Socket } from 'socket.io';

const app: Application = express();
const httpServer = createServer(app);
const io = new Server(httpServer);

app.get('/', (req, res) => {
    res.send('Hello World!');
});

io.on('connection', (socket: Socket) => {
    console.log('a user connected');
    socket.on('disconnect', () => {
        console.log('user disconnected');
    });
});

const PORT = process.env.PORT || 3000;
httpServer.listen(PORT, () => {
    console.log(`Server is running on port ${PORT}`);
});

'''
