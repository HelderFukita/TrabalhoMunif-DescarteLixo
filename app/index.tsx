import { Asset } from 'expo-asset';
import { router } from 'expo-router';
import React from 'react';
import {
  Linking,
  Platform,
  Pressable,
  StatusBar,
  StyleSheet,
  Text,
  View,
} from 'react-native';
import { SafeAreaView } from 'react-native-safe-area-context';
import { SvgUri } from 'react-native-svg';

const cameraLogoUri = Asset.fromModule(
  require('../assets/images/CameraLogoIcon.svg')
).uri;
const titleLogoUri = Asset.fromModule(
  require('../assets/images/TitleLogoIcon.svg')
).uri;

export default function IntroScreen() {
  const openSdgPage = async () => {
    const url = 'https://brasil.un.org/pt-br/sdgs';
    const canOpen = await Linking.canOpenURL(url);

    if (canOpen) {
      await Linking.openURL(url);
    }
  };

  return (
    <SafeAreaView style={styles.safeArea}>
      <StatusBar barStyle="light-content" />
      <View style={styles.container}>
        <View style={styles.card}>
          <View style={styles.logoGroup}>
            <SvgUri uri={cameraLogoUri} width={82} height={82} />
            <SvgUri uri={titleLogoUri} width={220} height={54} />
          </View>

          <Text style={styles.welcomeTitle}>Seja bem-vindo</Text>

          <Text style={styles.message}>Aponte a camera e descubra como descartar corretamente.</Text>
          <Text style={styles.message}>
            Cuidar do planeta pode ser simples e começa com pequenas escolhas.
          </Text>

          <Pressable
            style={({ pressed }) => [styles.startButton, pressed && styles.startButtonPressed]}
            onPress={() => router.push('/scan')}>
            <Text style={styles.startButtonText}>Iniciar classificação</Text>
          </Pressable>
        </View>

        <Pressable
          style={({ pressed }) => [styles.sdgBox, pressed && styles.sdgBoxPressed]}
          onPress={openSdgPage}>
          <Text style={styles.sdgLabel}>Importante</Text>
          <Text style={styles.sdgText}>Saiba mais sobre os Objetivos de Desenvolvimento Sustentavel</Text>
          <Text style={styles.sdgLink}>Acessar site da ONU Brasil</Text>
        </Pressable>
      </View>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  safeArea: {
    flex: 1,
    backgroundColor: '#071A26',
  },
  container: {
    flex: 1,
    paddingHorizontal: 18,
    paddingTop: 14,
    paddingBottom: 16,
    justifyContent: 'space-between',
    alignItems: 'center',
    gap: 14,
    backgroundColor: '#071A26',
  },
  card: {
    width: '100%',
    maxWidth: 480,
    backgroundColor: '#0E2A3A',
    borderWidth: 1,
    borderColor: '#174A63',
    borderRadius: 24,
    paddingHorizontal: 18,
    paddingVertical: 22,
    gap: 14,
    alignItems: 'center',
    marginTop: Platform.OS === 'web' ? 12 : 6,
  },
  logoGroup: {
    alignItems: 'center',
    gap: 8,
    marginBottom: 8,
  },
  welcomeTitle: {
    color: '#FFFFFF',
    fontSize: 30,
    lineHeight: 34,
    fontWeight: '800',
    textAlign: 'center',
  },
  message: {
    color: '#DCE9EF',
    fontSize: 16,
    lineHeight: 24,
    textAlign: 'center',
  },
  startButton: {
    width: '100%',
    backgroundColor: '#26C87A',
    borderRadius: 14,
    paddingVertical: 15,
    marginTop: 10,
    alignItems: 'center',
  },
  startButtonPressed: {
    opacity: 0.85,
    transform: [{ scale: 0.99 }],
  },
  startButtonText: {
    color: '#052017',
    fontSize: 17,
    fontWeight: '800',
  },
  sdgBox: {
    width: '100%',
    maxWidth: 480,
    borderRadius: 16,
    paddingHorizontal: 14,
    paddingVertical: 14,
    backgroundColor: '#0C2330',
    borderWidth: 1,
    borderColor: '#1E5D7C',
    gap: 4,
  },
  sdgBoxPressed: {
    opacity: 0.88,
  },
  sdgLabel: {
    color: '#7CCBFF',
    fontSize: 12,
    textTransform: 'uppercase',
    fontWeight: '700',
    letterSpacing: 0.4,
  },
  sdgText: {
    color: '#E8F2F7',
    fontSize: 14,
    lineHeight: 20,
    fontWeight: '500',
  },
  sdgLink: {
    marginTop: 2,
    color: '#4CC3FF',
    fontSize: 14,
    fontWeight: '700',
  },
});
