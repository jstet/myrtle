from transformers import TFAutoModelForCausalLM, AutoTokenizer
import tensorflow as tf

model_name = "jstet/myrtle"

tokenizer = AutoTokenizer.from_pretrained(model_name)
model = TFAutoModelForCausalLM.from_pretrained(model_name)


tflite_model = tf.lite.TFLiteConverter.from_keras_model(model).convert()
