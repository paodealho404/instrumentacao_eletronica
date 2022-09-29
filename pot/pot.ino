const int VOL_PIN = A0;
const int n = 8;
float factor[n] = {
    -1367.7683236907033, 4004.283865365811, -4208.839544576302,
    2362.56930138958, -775.694927869914, 149.17645538165743,
    -15.586238303975392, 0.6836451762256601}; // Coeficientes obtidos a partir
                                              // da aproximação utilizando o
                                              // método dos mínimos quadrados

// Variável de controle para impressão do valor de tensão ou valor de ângulo
// convertido
#define converter_angulo true

void setup()
{
  Serial.begin(9600);
}

void loop()
{
  long value = 0;
  float volt = 0;

  for (int i = 0; i < 100; i++)
  {
    value += analogRead(VOL_PIN);
    /* Entrada analógica(A/D) do arduino */
  }

  volt = value / 100 * 5.0 / 1023.0;
  /* Calculando a tensão média para obter uma melhor precisão */

  /*Algoritmo de Horner (Polinômio Forma Aninhada)*/
  float res_angle = factor[n - 1];
  for (int i = n - 1; i > 0; i--)
  {
    /* Cálculo do ângulo resultante através da tensão média e os coeficientes
     * aproximados  */
    res_angle = res_angle * volt + factor[i - 1];
  }

  if (converter_angulo)
  {
    Serial.println(String(res_angle));
  }
  else
  {
    Serial.println(String(volt));
  }

  delay(100);
}