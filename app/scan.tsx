import { router } from 'expo-router';
import React from 'react';
import { Platform, Pressable, StatusBar, StyleSheet, Text, View } from 'react-native';
import { SafeAreaView, useSafeAreaInsets } from 'react-native-safe-area-context';

import HomeScreen from './HomeScreen';

export default function ScanScreen() {
  const insets = useSafeAreaInsets();
  const isWeb = Platform.OS === 'web';

  return (
    <SafeAreaView style={styles.container} edges={['left', 'right']}>
      <StatusBar barStyle="light-content" translucent backgroundColor="transparent" />
      <HomeScreen />
      {isWeb && (
        <View style={[styles.headerOverlay, { top: insets.top + 12 }]} pointerEvents="box-none">
          <Pressable style={styles.backButton} onPress={() => router.replace('/')}>
            <Text style={styles.backButtonText}>Voltar</Text>
          </Pressable>
        </View>
      )}
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#000000',
  },
  headerOverlay: {
    position: 'absolute',
    left: 12,
    right: 12,
    zIndex: 20,
  },
  backButton: {
    alignSelf: 'flex-start',
    backgroundColor: '#0E2A3ACC',
    borderColor: '#1E5D7C',
    borderWidth: 1,
    borderRadius: 12,
    paddingVertical: 10,
    paddingHorizontal: 14,
  },
  backButtonText: {
    color: '#FFFFFF',
    fontSize: 15,
    fontWeight: '700',
  },
});
