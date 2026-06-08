import { CameraView, useCameraPermissions } from 'expo-camera';
import Constants from 'expo-constants';
import * as ImagePicker from 'expo-image-picker';
import React, { useEffect, useRef, useState } from 'react';
import {
  ActivityIndicator,
  Image,
  Platform,
  ScrollView,
  StyleSheet,
  Text,
  TextInput,
  TouchableOpacity,
  View,
} from 'react-native';
import { useSafeAreaInsets } from 'react-native-safe-area-context';

type DetectionResult = {
  class: string;
  class_pt?: string;
  confidence: number;
  disposal: string;
};

function getApiUrl() {
  const explicitUrl = process.env.EXPO_PUBLIC_API_URL?.trim();

  if (explicitUrl) {
    return explicitUrl.replace(/\/$/, '');
  }

  if (Platform.OS === 'web') {
    return 'http://localhost:5000';
  }

  const host = Constants.expoConfig?.hostUri?.split(':')[0];

  return host ? `http://${host}:5000` : 'http://localhost:5000';
}

function getFriendlyErrorMessage(error: unknown, fallback: string) {
  if (!(error instanceof Error)) {
    return fallback;
  }

  const message = error.message.trim();

  if (!message) {
    return fallback;
  }

  const isTechnicalMessage =
    /https?:\/\/\S+/i.test(message) ||
    /No connection adapters were found|Invalid URL|MissingSchema|InvalidSchema|Failed to parse|cannot identify image file|UnidentifiedImageError|timed out|ConnectionError/i.test(
      message,
    );

  return isTechnicalMessage ? fallback : message;
}

async function buildFormDataFromImage(uri: string, name: string, file?: File | Blob | null) {
  if (Platform.OS === 'web') {
    const formData = new FormData();
    const imageBlob = file ?? (await (await fetch(uri)).blob());

    formData.append('image', imageBlob, name);

    return formData;
  }

  const formData = new FormData();

  formData.append('image', {
    uri,
    name,
    type: 'image/jpeg',
  } as any);

  return formData;
}

export default function HomeScreen() {
  const insets = useSafeAreaInsets();
  const [permission, requestPermission] = useCameraPermissions();
  const cameraRef = useRef<any>(null);

  const [result, setResult] = useState<DetectionResult | null>(null);
  const [loading, setLoading] = useState(false);
  const [running, setRunning] = useState(false);
  const [errorMessage, setErrorMessage] = useState<string | null>(null);
  const [imageUrl, setImageUrl] = useState('');
  const [previewUri, setPreviewUri] = useState<string | null>(null);
  const reciclaveis = ['plastic', 'glass', 'paper', 'metal', 'cardboard'];
  const API_URL = getApiUrl();
  const isWeb = Platform.OS === 'web';

  useEffect(() => {
    if (!isWeb) {
      requestPermission();
    }
  }, [isWeb, requestPermission]);

  const sendImageToBackend = async (uri: string, name: string, file?: File | Blob | null) => {
    const formData = await buildFormDataFromImage(uri, name, file);

    const response = await fetch(`${API_URL}/detect`, {
      method: 'POST',
      body: formData,
    });

    const data = await response.json();

    if (!response.ok) {
      throw new Error(data?.error ?? 'Falha ao processar a imagem');
    }

    setResult(data);
  };

  const sendImageUrlToBackend = async () => {
    const normalizedUrl = imageUrl.trim();

    if (!normalizedUrl) {
      setErrorMessage('Digite a URL de uma imagem.');
      return;
    }

    try {
      setLoading(true);
      setErrorMessage(null);
      setResult(null);
      setPreviewUri(normalizedUrl);

      const response = await fetch(`${API_URL}/detect`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ url: normalizedUrl }),
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data?.error ?? 'Falha ao processar a URL da imagem');
      }

      setResult(data);
    } catch (err) {
      setErrorMessage(getFriendlyErrorMessage(err, 'Falha ao enviar URL da imagem'));
    } finally {
      setLoading(false);
    }
  };

  const captureAndSend = async () => {
    if (!cameraRef.current) return;

    try {
      setLoading(true);
      setErrorMessage(null);

      const photo = await cameraRef.current.takePictureAsync({
        base64: false,
        quality: 0.5,
      });

      await sendImageToBackend(photo.uri, 'frame.jpg');
    } catch (err) {
      setErrorMessage(getFriendlyErrorMessage(err, 'Falha ao capturar a imagem'));
    } finally {
      setLoading(false);
    }
  };

  const pickImageFromLibrary = async () => {
    try {
      setLoading(true);
      setErrorMessage(null);
      setImageUrl('');
      setResult(null);
      setPreviewUri(null);

      const imageResult = await ImagePicker.launchImageLibraryAsync({
        mediaTypes: ImagePicker.MediaTypeOptions.Images,
        quality: 0.8,
      });

      if (imageResult.canceled || !imageResult.assets[0]) {
        return;
      }

      const asset = imageResult.assets[0];

      setPreviewUri(asset.uri);

      await sendImageToBackend(asset.uri, asset.fileName ?? 'upload.jpg', (asset as any).file);
    } catch (err) {
      setErrorMessage(getFriendlyErrorMessage(err, 'Falha ao selecionar a imagem'));
    } finally {
      setLoading(false);
    }
  };

  // Loop "tempo real"
  useEffect(() => {
    let interval: any;

    if (running) {
      interval = setInterval(() => {
        captureAndSend();
      }, 1500); // ⏱️ a cada 1.5s
    }

    return () => clearInterval(interval);
  }, [running]);

  const toggleDetection = () => {
    if (!running) {
      setPreviewUri(null);
    }

    setRunning((previous) => !previous);
  };

  if (!isWeb && !permission) return <View />;
  if (!isWeb && !permission?.granted) {
    return (
      <View style={styles.center}>
        <Text>Permissão da câmera necessária</Text>
      </View>
    );
  }

  return (
    <View style={styles.container}>
      {!isWeb ? (
        <CameraView ref={cameraRef} style={styles.camera} />
      ) : (
        <ScrollView style={styles.webScroll} contentContainerStyle={styles.webScrollContent}>
          <View style={styles.webCard}>
            <Text style={styles.webTitle}>Detecção no navegador</Text>
            <Text style={styles.webSubtitle}>
              No web, selecione uma imagem local ou informe uma URL pública para obter a classificação.
            </Text>

            <TextInput
              value={imageUrl}
              onChangeText={(value) => {
                setImageUrl(value);
                setPreviewUri(null);
                setResult(null);
              }}
              placeholder="https://site.com/imagem.jpg"
              placeholderTextColor="#98A2B3"
              autoCapitalize="none"
              autoCorrect={false}
              keyboardType="url"
              style={styles.urlInput}
            />

            <View style={styles.webActionsRow}>
              <TouchableOpacity style={styles.webUrlButton} onPress={sendImageUrlToBackend}>
                <Text style={styles.buttonText}>Detectar por URL</Text>
              </TouchableOpacity>

              <TouchableOpacity style={styles.webButton} onPress={pickImageFromLibrary}>
                <Text style={styles.buttonText}>Selecionar imagem</Text>
              </TouchableOpacity>
            </View>

            {errorMessage && <Text style={styles.errorInline}>{errorMessage}</Text>}

            {previewUri && (
              <View style={styles.previewWrapper}>
                <Text style={styles.previewLabel}>Pré-visualização</Text>
                <Image source={{ uri: previewUri }} style={styles.previewImage} resizeMode="cover" />
              </View>
            )}

            {result && (
              <View style={styles.webResultCard}>
                <Text style={styles.webResultTitle}>Resultado</Text>
                <Text style={styles.webResultText}>
                  Classe: <Text style={styles.bold}>{result.class_pt ?? result.class}</Text>
                </Text>
                <Text style={styles.webResultText}>
                  Confiança: <Text style={styles.bold}>{(result.confidence * 100).toFixed(2)}%</Text>
                </Text>
                <Text style={styles.disposal}>{result.disposal}</Text>
                <Text style={styles.disposal}>
                  {reciclaveis.includes(result.class)
                    ? '♻️ Material reciclável'
                    : '❌ Não reciclável'}
                </Text>
              </View>
            )}
          </View>
        </ScrollView>
      )}

      {!isWeb && (
        <View style={[styles.mobileActions, { bottom: insets.bottom + 40 }]}>
          {previewUri && (
            <View style={styles.mobilePreviewWrapper}>
              <Text style={styles.mobilePreviewLabel}>Imagem importada</Text>
              <Image source={{ uri: previewUri }} style={styles.mobilePreviewImage} resizeMode="cover" />
            </View>
          )}

          <TouchableOpacity style={styles.importButton} onPress={pickImageFromLibrary}>
            <Text style={styles.buttonText}>Importar imagem</Text>
          </TouchableOpacity>

          <TouchableOpacity style={styles.button} onPress={toggleDetection}>
            <Text style={styles.buttonText}>{running ? 'Parar' : 'Iniciar Detecção'}</Text>
          </TouchableOpacity>
        </View>
      )}

      {loading && (
        <View style={styles.loadingOverlay}>
          <ActivityIndicator size="large" color="#ffffff" />
          <Text style={styles.loadingText}>Processando imagem...</Text>
        </View>
      )}

      {!isWeb && errorMessage && <Text style={styles.error}>{errorMessage}</Text>}

      {!isWeb && result && (
        <View style={styles.result}>
          <Text style={styles.text}>
            Classe: <Text style={styles.bold}>{result.class_pt ?? result.class}</Text>
          </Text>

          <Text style={styles.text}>
            Confiança:{' '}
            <Text style={styles.bold}>
              {(result.confidence * 100).toFixed(2)}%
            </Text>
          </Text>

          <Text style={styles.disposal}>{result.disposal}</Text>
          <Text style={styles.disposal}>
            {reciclaveis.includes(result.class)
              ? '♻️ Material reciclável'
              : '❌ Não reciclável'}
          </Text>
        </View>
      )}
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1 },
  camera: { flex: 1 },

  webScroll: {
    flex: 1,
    backgroundColor: '#0B1220',
  },

  webScrollContent: {
    flexGrow: 1,
    paddingVertical: 28,
    paddingHorizontal: 16,
    alignItems: 'center',
  },

  webCard: {
    width: '100%',
    maxWidth: 860,
    backgroundColor: '#101828',
    borderRadius: 18,
    padding: 22,
    borderWidth: 1,
    borderColor: '#344054',
    gap: 14,
  },

  webContainer: {
    flex: 1,
    padding: 24,
    justifyContent: 'center',
    alignItems: 'center',
    gap: 16,
    backgroundColor: '#101828',
  },

  webTitle: {
    color: '#ffffff',
    fontSize: 30,
    fontWeight: 'bold',
    textAlign: 'left',
  },

  webSubtitle: {
    color: '#d0d5dd',
    fontSize: 16,
    textAlign: 'left',
    lineHeight: 22,
  },

  webActionsRow: {
    width: '100%',
    flexDirection: 'row',
    flexWrap: 'wrap',
    gap: 10,
  },

  webButton: {
    backgroundColor: '#4CAF50',
    paddingVertical: 14,
    paddingHorizontal: 24,
    borderRadius: 12,
    minWidth: 190,
  },

  webUrlButton: {
    backgroundColor: '#1570EF',
    paddingVertical: 14,
    paddingHorizontal: 24,
    borderRadius: 12,
    minWidth: 190,
  },

  urlInput: {
    width: '100%',
    maxWidth: 560,
    backgroundColor: '#FFFFFF',
    color: '#101828',
    borderRadius: 10,
    paddingHorizontal: 14,
    paddingVertical: 12,
    fontSize: 15,
  },

  previewWrapper: {
    width: '100%',
    maxWidth: 720,
    marginTop: 8,
  },

  previewLabel: {
    color: '#ffffff',
    fontSize: 14,
    marginBottom: 8,
    fontWeight: '600',
  },

  previewImage: {
    width: '100%',
    minHeight: 220,
    height: 320,
    borderRadius: 12,
    backgroundColor: '#344054',
  },

  webResultCard: {
    width: '100%',
    backgroundColor: '#0C111D',
    borderRadius: 14,
    padding: 16,
    borderWidth: 1,
    borderColor: '#344054',
  },

  webResultTitle: {
    color: '#98A2B3',
    fontSize: 13,
    textTransform: 'uppercase',
    marginBottom: 8,
    letterSpacing: 0.8,
  },

  webResultText: {
    color: '#F2F4F7',
    fontSize: 16,
    marginBottom: 6,
  },

  mobileActions: {
    position: 'absolute',
    left: 16,
    right: 16,
    gap: 10,
  },

  mobilePreviewWrapper: {
    backgroundColor: '#0C111DCC',
    borderWidth: 1,
    borderColor: '#344054',
    borderRadius: 12,
    padding: 8,
  },

  mobilePreviewLabel: {
    color: '#FFFFFF',
    fontSize: 12,
    fontWeight: '700',
    marginBottom: 6,
  },

  mobilePreviewImage: {
    width: '100%',
    height: 120,
    borderRadius: 8,
    backgroundColor: '#1F2937',
  },

  button: {
    backgroundColor: '#4CAF50',
    padding: 15,
    borderRadius: 10,
    alignItems: 'center',
  },

  importButton: {
    backgroundColor: '#1570EF',
    padding: 15,
    borderRadius: 10,
    alignItems: 'center',
  },

  buttonText: {
    color: '#fff',
    fontWeight: 'bold',
  },

  loadingOverlay: {
    position: 'absolute',
    top: 0,
    bottom: 0,
    left: 0,
    right: 0,
    backgroundColor: '#00000055',
    justifyContent: 'center',
    alignItems: 'center',
    zIndex: 99,
  },

  loadingText: {
    marginTop: 12,
    color: '#ffffff',
    fontSize: 14,
    fontWeight: '600',
  },

  error: {
    position: 'absolute',
    top: 24,
    left: 20,
    right: 20,
    backgroundColor: '#8b1e3f',
    color: '#fff',
    padding: 12,
    borderRadius: 10,
    textAlign: 'center',
  },

  errorInline: {
    backgroundColor: '#8b1e3f',
    color: '#fff',
    padding: 12,
    borderRadius: 10,
    textAlign: 'left',
  },

  result: {
    position: 'absolute',
    top: 60,
    left: 20,
    right: 20,
    backgroundColor: '#000000aa',
    padding: 15,
    borderRadius: 10,
  },

  text: {
    color: '#fff',
    fontSize: 16,
  },

  bold: {
    fontWeight: 'bold',
  },

  disposal: {
    marginTop: 5,
    color: '#00ff88',
    fontWeight: 'bold',
  },

  center: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
  },
});