# Outlier.ai — Cheat Sheet para Verificación de Skills

> Para cuando Emi haga la skills verification en Outlier.
> Basado en experiencia real de Emilio (identity.json).

## Perfil a configurar

**Role**: Python Developer / ML Engineer
**Headline**: Systems Engineer | Data Scientist | Python | ML
**Experience level**: Senior (5+ años profesionales comprobables)

## Tips generales

1. **Usá Chrome con la sesión de Emilio** — ya está logueado en Outlier
2. **La verificación de skills suele ser**: un assessment técnico (Python/ML) + preguntas de experiencia
3. **Tomátelo con calma**: podés pausar y retomar
4. **Hacelo en un horario tranquilo** — no de madrugada

## Temas que suelen aparecer (Python General)

### List comprehensions vs loops
```python
# Más eficiente
squares = [x**2 for x in range(10)]

# vs
squares = []
for x in range(10):
    squares.append(x**2)
```

### Manejo de excepciones
```python
try:
    result = risky_operation()
except ValueError as e:
    log.error(f"Value error: {e}")
    return None
except Exception as e:
    log.error(f"Unexpected: {e}")
    raise
finally:
    cleanup()
```

### Decorators básicos
```python
from functools import wraps

def timing_decorator(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        print(f"{func.__name__} took {time.time()-start:.2f}s")
        return result
    return wrapper
```

### Generators vs listas
```python
# Generator (memoria eficiente)
def read_large_file(file_path):
    with open(file_path) as f:
        for line in f:
            yield line.strip()

# Uso
for line in read_large_file("data.csv"):
    process(line)
```

## Temas de ML que suelen aparecer

### Train/Test split
```python
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)
```

### Pipeline típico
```python
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier

pipeline = Pipeline([
    ('scaler', StandardScaler()),
    ('classifier', RandomForestClassifier(n_estimators=100))
])
pipeline.fit(X_train, y_train)
```

### Métricas clave
```python
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix

y_pred = model.predict(X_test)
print(f"Accuracy: {accuracy_score(y_test, y_pred):.3f}")
print(f"Precision: {precision_score(y_test, y_pred, average='weighted'):.3f}")
print(f"Recall: {recall_score(y_test, y_pred, average='weighted'):.3f}")
```

### Cross-validation
```python
from sklearn.model_selection import cross_val_score
scores = cross_val_score(model, X, y, cv=5, scoring='accuracy')
print(f"CV Accuracy: {scores.mean():.3f} (+/- {scores.std()*2:.3f})")
```

## Temas de SQL (si aparecen)

```sql
-- JOIN con agregación
SELECT 
    c.customer_id,
    c.name,
    COUNT(o.order_id) as order_count,
    SUM(o.amount) as total_spent
FROM customers c
LEFT JOIN orders o ON c.customer_id = o.customer_id
WHERE o.order_date >= '2024-01-01'
GROUP BY c.customer_id, c.name
HAVING COUNT(o.order_id) > 5
ORDER BY total_spent DESC;

-- Window function
SELECT 
    department,
    employee_name,
    salary,
    RANK() OVER (PARTITION BY department ORDER BY salary DESC) as rank
FROM employees;
```

## Lo que NO hacer
- No inventar experiencia que no tenés (rk-verify-claims.py después)
- No decir "10+ años en React" — no es tu stack
- Ser honesto con lo que sabés: sos fuerte en Python, ML, SQL, BI
- Si te preguntan por years of experience: 10+ años total en tech (desde 2015), 3+ años específicos en data/ML

## Después de la verificación
- Si pasa: avisame y configuro las alertas de tasks disponibles
- Si no pasa: vemos qué área falló y preparamos específico
