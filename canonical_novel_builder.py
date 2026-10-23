import os
import sys
from epub_builder import create_epub

def build_complete_canonical_novel():
    print("Iniciando compilación de la Obra Completa: Arquímedes // Libro I: La Voluntad de las Cenizas...")
    
    passages = [
        {
            "chapter_number": 0,
            "chapter_title": "Prólogo: El Péndulo de Niebla",
            "act_title": "Acto I: La Puerta de Hierro y Ceniza",
            "narrative": """El olor del vapor ionizado fue lo primero en abrirse paso a través de la inconsciencia. Era un hedor químico y punzante, como a cobre recalentado en el vacío, mezclado con el hedor acre del aislante polimérico derretido.

Oscar abrió los párpados con lentitud. Las luces de emergencia del hangar de simuladores bañaban las mamparas de titanio en un resplandor estroboscópico de color ámbar. A intervalos regulares de tres segundos, una sirena sorda vibraba en el suelo de rejilla metálica, haciendo temblar los pernos bajo sus botas. El Reactor Geller, enterrado en el vientre de la instalación militar, emitía un zumbido disonante que no pertenecía al rango auditivo humano estándar, sino que resonaba directamente contra la corteza occipital de los presentes.

A tres metros de donde yacía, una figura se incorporó con una frialdad perturbadora. La cadete vestía el mismo mono presurizado de instrucción táctica con el emblema de la Academia Ares, pero sus movimientos carecían por completo de la desorientación biológica habitual tras una descompresión súbita. Sus cabellos plateados caían en mechones precisos sobre los hombros, y sus ojos —grises, refractarios como el vidrio blindado— barrieron la sala hasta clavarse en Oscar.

—Levántate, cadete —dijo Virginia. Su voz era un susurro seco, cortante como una cuchilla quirúrgica, perfectamente audible por encima de las sirenas de evacuación—. Si permaneces en esa rejilla cuando el protocolo de sellado concluya, los eyectores de argón licuado congelarán tus pulmones en menos de cuatro segundos.

Oscar intentó apoyar la mano izquierda en el mamparo, pero una descarga estática le recorrió el antebrazo. Miró su cronógrafo de pulsera: los dígitos de cuarzo no avanzaban; retrocedían de forma espasmódica, descontando fracciones de segundo que no existían. Aquel no era un simulacro de la Academia. Algo fundamental en el tejido de la realidad acababa de romperse."""
        },
        {
            "chapter_number": 1,
            "chapter_title": "Capítulo 1: El Umbral de la Academia",
            "act_title": "Acto I: La Puerta de Hierro y Ceniza",
            "narrative": """La Puerta de Hierro y Ceniza era una mole ciclópea de trescientos metros de altura que partía en dos la cordillera volcánica de Ares Prime. Durante más de un siglo, la doctrina militar imperial había sostenido que tras ese portón no ingresaban hombres, sino materia prima para la guerra. Cien aspirantes habían marchado al amanecer bajo la lluvia ácida; al mediodía, solo cuarenta continuaban en pie en la explanada de clasificación.

El Instructor Kaelen se detuvo frente a Oscar. Vestía el uniforme de cuero endurecido y blindaje cerámico de la Guardia de Inspección, con las condecoraciones de la Campaña del Velo pendiendo de su pecho como colmillos de metal negro. Su ojo biónico emitió un chasquido servoasistido al escanear los signos biométricos del cadete.

—Tu ritmo cardíaco se mantiene en cincuenta y ocho pulsaciones por minuto, recluta —espetó Kaelen con desprecio contenido—. O eres demasiado estúpido para comprender la magnitud de lo que te aguarda en los simuladores neuronales, o tu implante occipital está filtrando datos sin autorización. En ambos casos, eres una variable que la Academia no tolera.

—Solo sigo el protocolo de respiración de combate prescrito en el Manual de Maniobras, señor —respondió Oscar, manteniendo la mirada fija en el horizonte de chimeneas humeantes, sin parpadear.

Kaelen sonrió sin calidez. A unos metros de distancia, en la fila de selección, Virginia no apartaba la mirada de ambos. En su mano derecha sostenía un pequeño cilindro de datos con el sello borrado, un artefacto que ningún recluta de nuevo ingreso debería haber poseído jamás. La inspección continuó, pero la advertencia quedó grabada en el aire: en la Academia Ares, sobrevivir al primer día exigía ocultar tanto las debilidades como cualquier síntoma de excepcionalidad."""
        },
        {
            "chapter_number": 2,
            "chapter_title": "Capítulo 2: Los Simuladores de Vacío",
            "act_title": "Acto I: La Puerta de Hierro y Ceniza",
            "narrative": """Las cápsulas de inmersión sináptica se alineaban en la galería del Nivel Sub-3 como sarcófagos de aleación oscura suspendidos sobre un abismo de cables de fibra óptica. El aire allí abajo era gélido, diseñado para disipar el calor colosal producido por los ordenadores cuánticos de la era anterior al colapso.

Cuando la escotilla de la cápsula número siete se selló herméticamente sobre Oscar, la oscuridad fue absoluta durante un segundo. Luego vino la aguja. El conector neuroespinal penetró en la base de su cráneo con un chasquido seco y una llamarada fría de dolor que le contrajo la mandíbula. De golpe, sus sentidos físicos se desvanecieron, reemplazados por el vacío infinito del espacio táctico y las trazas telemétricas de una escuadra enemiga en aproximación orbital.

En la simulación estándar, cada cadete combatía en solitario. Sin embargo, en el cuadrante periférico del radar de Oscar apareció un vector no asignado por el instructor: una señal encriptada con firma biológica sincronizada.

«No intentes maniobrar hacia el cinturón de escombros, Oscar», resonó la voz de Virginia directamente en su córtex auditivo, burlando los cortafuegos del sistema militar. «Los algoritmos de Kaelen han configurado un cuello de botella de torpedos guiados en las coordenadas Delta-Nueve. Quieren forzar una baja simulada para justificar tu purga del escuadrón.»

Oscar no respondió por voz; en su lugar, ejecutó una maniobra evasiva en espiral descendente hacia la sombra térmica del reactor de la estación simulada. La aguja de entropía en su consola parpadeó en rojo. Por primera vez, Oscar comprendió que los simuladores no estaban creando escenarios ficticios: estaban extrayendo memorias de batallas pasadas que la historia oficial afirmaba que nunca habían ocurrido."""
        },
        {
            "chapter_number": 3,
            "chapter_title": "Capítulo 3: La Jerarquía de las Sombras",
            "act_title": "Acto I: La Puerta de Hierro y Ceniza",
            "narrative": """El comedor de cadetes del Nivel Sub-4 no ofrecía tregua alguna. Bajo los fluorescentes zumbantes que parpadeaban con la frecuencia inestable de la red energética, los aspirantes se agrupaban en castas rígidas: los vástagos de las familias patricias de la capital en las mesas centrales, y los reclutas de las colonias mineras en los márgenes de hormigón desnudo.

El Cadete Reyes arrojó su bandeja de rancho sobre la mesa donde Oscar revisaba sus diagramas tácticos. Reyes era dos cabezas más alto que la media, con cicatrices de combate en el cuello y la arrogancia de quien sabe que su linaje posee tres acorazados en la flota del Núcleo.

—Me han dicho que tu cápsula registró una tasa de supervivencia del noventa y dos por ciento en la prueba del vacío —dijo Reyes, inclinándose con una sonrisa tensa y amenazante—. En mi escuadra no toleramos que un paria del cinturón de cenizas altere la curva de calificación. Esta noche habrá una revisión física en las duchas del bloque C. Asegúrate de venir desarmado.

Antes de que Oscar pudiera responder, una mano delgada y enguantada se posó sobre el hombro de Reyes. La fuerza del agarre hizo que el gigante parpadeara de dolor. Virginia estaba detrás de él, con su vaso de agua intacto en la otra mano y una expresión de aburrimiento glacial.

—Si tocas a este cadete antes de la medianoche, Reyes, el Instructor Kaelen revisará los registros de acceso al almacén de municiones del hangar secundario —dijo Virginia con serenidad letal—. Y ambos sabemos qué firma biométrica desactivó las cámaras de seguridad ayer a las cero trescientas horas.

Reyes palideció. Dio dos pasos atrás, miró con furia alternada a Oscar y a Virginia, y se retiró con su séquito hacia las sombras del pasillo. Oscar alzó la mirada hacia su compañera:

—¿Cómo sabías lo de las cámaras? —preguntó.

Virginia tomó asiento frente a él y bebió un sorbo de agua antes de contestar en voz baja:
—Porque en la última repetición, tú no sobreviviste a la emboscada de las duchas. Y no pienso permitir que muramos de nuevo por culpa de un matón de tercera categoría."""
        },
        {
            "chapter_number": 4,
            "chapter_title": "Capítulo 4: Las Ruinas Ciclópeas Subterráneas",
            "act_title": "Acto I: La Puerta de Hierro y Ceniza",
            "narrative": """La asignación nocturna de limpieza en el sector de desagües parecía un castigo rutinario, pero Virginia la había seleccionado deliberadamente sobornando al suboficial de guardia con una ración de estimulantes sintéticos.

Descendieron por escaleras de caracol metálicas que parecían no tener fin, dejando atrás las secciones de hormigón prefabricado de la Academia moderna. A trescientos metros de profundidad, la arquitectura cambió de manera radical y desconcertante: las paredes ya no estaban hechas de placas remachadas, sino de un material monolítico, negro y pulido como la obsidiana, que absorbía los haces de las linternas tácticas sin reflejar un solo fotón.

—Esto no lo construyeron nuestros ingenieros —murmuró Oscar, pasando los dedos enguantados por los bajorrelieves que recorrían el dintel de una galería colosal. No eran letras ni inscripciones técnicas; eran patrones de interferencia de ondas, diagramas de campos gravitatorios congelados en piedra metamórfica.

—La Academia fue levantada aquí no para entrenar pilotos, sino para custodiar este enclave —explicó Virginia, consultando un escáner portátil con lecturas fluctuantes—. Hace cuatrocientos años, la expedición que descubrió este planeta creyó encontrar depósitos minerales. Lo que hallaron fue una máquina de contención de probabilidad. La llamaron el Proyecto Arquímedes.

Al final de la galería, una hendidura luminiscente en el suelo latía con un fulgor azul pálido. De su interior ascendía una corriente de aire tibio con aroma a ozono y flores marchitas, un olor imposible en un búnker subterráneo militar. Oscar se inclinó sobre el borde: en el fondo de la sima, flotando sin soporte visible, giraba un cilindro de doce facetas cubierto de runas electromagnéticas. Al mirarlo, un dolor punzante le atravesó las sienes: no estaba viendo un objeto físico, estaba contemplando un nudo en el tiempo."""
        },
        {
            "chapter_number": 5,
            "chapter_title": "Capítulo 5: El Secreto del Reactor Geller",
            "act_title": "Acto I: La Puerta de Hierro y Ceniza",
            "narrative": """La infiltración en la subestación de control del Reactor Geller requirió cruzar tres esclusas de vacío con credenciales sustraídas de los archivos del Prefecto. El calor allí dentro era asfixiante; las bombas de refrigerante de sodio líquido rugían con un gemido continuo que amortiguaba los pasos de ambos cadetes.

Frente a la consola maestra, Oscar conectó el terminal de derivación que Virginia le extendió. Las pantallas de fósforo verde cobraron vida, vomitando cascadas de registros clasificados bajo el sello de Ultra Máximo Secreto.

—Mira estos registros —señaló Oscar con la respiración entrecortada—. Las fechas de los informes de incidentes. Hay reportes de explosiones en el reactor con fecha de mañana. Y de la semana que viene. Y del año pasado con nuestros mismos nombres registrados en la lista de bajas.

Virginia no mostró sorpresa; sus ojos escrutaban las columnas de telemetría de entropía.
—El reactor no produce energía para la base, Oscar. El reactor absorbe el impacto de las fluctuaciones cuánticas provocadas por la máquina que vimos abajo. Cada vez que el Alto Mando intenta activar el núcleo para alterar el curso de la guerra en el sector Ares, la realidad se colapsa por exceso de masa temporal. Y cuando la masa temporal sobrepasa el límite crítico, el sistema dispara un pulso de retroceso ontológico.

—Un bucle —comprendió Oscar con un escalofrío que le erizó la piel—. Todo este lugar... las pruebas, las órdenes de Kaelen, los cadetes muriendo en los simuladores... estamos atrapados en un círculo cerrado de cenizas.

En ese instante, una luz roja comenzó a girar en el techo de la cámara. La voz metálica del sintetizador de seguridad resonó en todos los altavoces:
«Alerta de Brecha Nivel Uno. Intrusión no autorizada en el Núcleo Geller. Protocolo de Exterminio Inmediato activado.»"""
        },
        {
            "chapter_number": 6,
            "chapter_title": "Capítulo 6: La Fuga de los Ecos",
            "act_title": "Acto I: La Puerta de Hierro y Ceniza",
            "narrative": """Las compuertas blindadas del pasillo principal comenzaron a descender con estruendo hidráulico. Detrás de ellos, los primeros disparos de rifle cinético arrancaron chispas incandescentes de las paredes de acero. Los centinelas de la Guardia Pretoriana avanzaban con visores infrarrojos y rifles de pulsos pesados en formación de barrido.

—¡Por los conductos de refrigeración auxiliar! —gritó Oscar, disparando con una pistola de pernos que había arrebatado a un centinela caído. El perno atravesó el servomotor de una válvula de presión, liberando una nube densa de vapor supercalentado que cegó a los guardias que venían a la zaga.

Virginia corría a su lado con una agilidad matemática. No dudaba en ninguna bifurcación; saltaba sobre tuberías incandescentes y se deslizaba bajo mamparos a medio cerrar como si conociera de antemano el segundo exacto en que cada mecanismo caería.

—¡Dobla a la izquierda en la siguiente intersección! —ordenó ella.
—¡La izquierda lleva al colector de residuos del reactor, es un callejón sin salida! —replicó Oscar mientras las balas silbaban sobre sus cabezas.
—¡En esta iteración aún no han cerrado la compuerta manual de mantenimiento! —le gritó Virginia sin detenerse—. ¡Confía en mí o muere aquí mismo!

Oscar apretó los dientes y se arrojó tras ella al cruce izquierdo. La compuerta, en efecto, estaba trabada por una barra de torsión caída. Se arrastraron a través del estrecho espacio milisegundos antes de que una ráfaga de proyectiles de fragmentación pulverizara el marco de acero donde habían estado parados. En la oscuridad del conducto de servicio, jadeando con los pulmones ardiendo por los gases tóxicos, se miraron en silencio. La distancia entre ellos se había disuelto: ya no eran dos cadetes rivales; eran los únicos dos seres conscientes en un tablero que repetía su propia matanza."""
        },
        {
            "chapter_number": 7,
            "chapter_title": "Capítulo 7: La Alianza de las Cenizas",
            "act_title": "Acto I: La Puerta de Hierro y Ceniza",
            "narrative": """En la cámara estanca de la torre de enfriamiento abandonada, el viento exterior ululaba a través de las rendijas de escape, trayendo el olor a ceniza volcánica y lluvia ácida de la superficie de Ares Prime.

Oscar se sentó contra un panel de control desactivado, vendándose el antebrazo izquierdo donde una esquirla de metralla le había abierto un surco sangrante. Virginia se arrodilló frente a él, sacó un inyector dérmico de su cartuchera y le aplicó una dosis de coagulante sin pedir permiso. El ardor fue instantáneo, seguido de un alivio helado.

—¿Cuántas veces hemos muerto en esta instalación, Virginia? —preguntó Oscar, mirándola directamente a los ojos.

Ella sostuvo la mirada sin pestañear. Por primera vez, una fisura de fatiga humana apareció en su compostura de hierro.
—Para mí, esta es la vigésima séptima ocasión en que llego a este pasillo contigo. Para ti, es la primera en que logras retener fragmentos de memoria después del colapso del reactor.

—¿Por qué yo? —insistió él—. Había cadetes más fuertes, estrategas con implantes de combate de última generación, pilotos con miles de horas de simulación. Yo solo soy un aspirante ordinario de las colonias.

—Porque todos los demás intentan obedecer o intentan escapar —respondió Virginia con voz queda pero rotunda—. Ninguno de ellos intentó entender qué sostenía la estructura. Arquímedes dijo: 'Dame un punto de apoyo y moveré el mundo'. La Academia no busca soldados para ganar una guerra exterior; busca un anclaje biológico capaz de estabilizar la máquina antes de que el universo colapse sobre sí mismo. Y tú eres el único cuyo córtex no se quema en el proceso.

Oscar miró su mano vendada y luego el horizonte de chimeneas que ardían en la noche a través de la rendija.
—Entonces no escaparemos de la Academia —dijo con resolución sombría—. Vamos a descender hasta el núcleo y vamos a forzar al reactor a mostrarnos la verdad completa."""
        },
        {
            "chapter_number": 8,
            "chapter_title": "Capítulo 8: La Fractura Ontológica",
            "act_title": "Acto I: La Puerta de Hierro y Ceniza",
            "narrative": """La sala del Núcleo Primario era una catedral de proporciones descomunales suspendida en el vacío del cráter volcánico. En el centro de la sala, sostenido por cuatro brazos magnéticos colosales, flotaba el artefacto: una esfera de aleación negra rodeada por anillos de luz blanca que giraban a velocidades hiperlumínicas, distorsionando el espacio a su alrededor hasta que las líneas rectas parecían quebrarse en ángulos imposibles.

El Instructor Kaelen los aguardaba en la pasarela central. A su lado se encontraban doce soldados de élite de la Guardia Imperial con rifles pesados amartillados.

—Habéis llegado más lejos de lo previsto, cadetes —dijo Kaelen. Su voz no contenía ira, sino una frialdad casi reverente—. Pero la prueba del Acto I ha concluido. El Alto Mando exige la purga de los especímenes que muestran divergencia conductual. Entregad los cilindros de datos y vuestras muertes serán registradas con honores en el Libro de Bajas de la República.

Oscar dio un paso al frente, pero no alzó las manos.
—Sabemos lo que hace la máquina, Kaelen —declaró Oscar con voz firme que resonó en el abismo—. El reactor no está conteniendo una explosión. Está rebobinando la masacre de Ares cada vez que el Imperio pierde el control del sector. No eres un instructor militar; eres el carcelero de un cementerio que se niega a permanecer enterrado.

Kaelen alzó su mano enguantada para ordenar abrir fuego. Pero antes de que los rifles dispararan, Virginia presionó el gatillo manual de sobrecarga que había conectado en la consola de refrigeración.

El sonido no fue una explosión convencional. Fue una rasgadura del tejido del silencio. La luz blanca envolvió la sala entera; la gravedad se invirtió instantáneamente; los cuerpos de los soldados, las pasarelas de acero y el propio Kaelen se disolvieron en fractales de ceniza brillante. Oscar sintió cómo sus recuerdos, sus huesos y su propia conciencia se desintegraban en una espiral infinita de ecos temporales. Pero esta vez, no cerró los ojos."""
        },
        {
            "chapter_number": 9,
            "chapter_title": "Capítulo 9: El Retorno al Umbral (El Despertar Consciente)",
            "act_title": "Acto I: La Puerta de Hierro y Ceniza",
            "narrative": """El vapor ionizado volvió a llenar sus pulmones. El olor a cobre recalentado. El silbido agudo de las sirenas de emergencia a tres segundos de intervalo.

Oscar abrió los ojos. Yacía en la rejilla del hangar de simuladores, exactamente en la misma posición de la primera escena. Pero esta vez no hubo desorientación ni mareo. Sus pupilas se contrajeron con una lucidez feroz. Miró su cronógrafo: los dígitos retrocedían exactamente como antes, pero ahora conocía el algoritmo de compensación.

Se puso de pie de un solo movimiento ágil y seguro antes de que la alarma de evacuación completara su primer ciclo.

Al otro lado del hangar, la cadete de cabello plateado comenzaba a incorporarse. Sus labios se abrieron para pronunciar las palabras que había repetido veintisiete veces:
—Levántate, cadete. Si permaneces en esa rejilla cuando el protocolo de sellado concluya...

—...los eyectores de argón licuado congelarán mis pulmones en menos de cuatro segundos —completó Oscar con voz tranquila, caminando con paso firme hacia ella—. Lo sé, Virginia. Y esta vez no vamos a perder diez minutos en la esclusa del Nivel Sub-3.

Virginia se congeló a mitad de frase. Sus ojos grises se abrieron con un asombro genuino y estremecedor que borró por completo su máscara de hielo. Miró las manos de Oscar, miró su postura y comprendió al instante: el bucle ya no era una prisión unipersonal. El catalizador se había activado.

Una leve, casi imperceptible sonrisa curvó la comisura de sus labios.
—Por fin —susurró ella—. Por fin estás despierto, Oscar."""
        },
        {
            "chapter_number": 10,
            "chapter_title": "Capítulo 10: Epílogo: La Voluntad de las Cenizas",
            "act_title": "Acto I: La Puerta de Hierro y Ceniza",
            "narrative": """Afuera, la lluvia ácida golpeaba los muros ciclópeos de la Puerta de Hierro y Ceniza con la fuerza de un diluvio eterno. Las chimeneas del complejo militar vomitaban fuego y humo sobre el cielo púrpura de Ares Prime, mientras los transportes blindados de la Guardia de Inspección se desplegaban en la plaza de armas para iniciar la selección matutina.

En el pasillo de servicio del Nivel Sub-1, al resguardo de las cámaras cuyos ángulos ciegos ahora dominaban con precisión milimétrica, Oscar y Virginia ajustaron los sellos de sus trajes de combate.

—Kaelen intentará emboscarnos en la galería de los simuladores a las trece cero cero horas —dijo Oscar, revisando el perno cinético en su pistolera—. Y el Cadete Reyes intentará interceptarnos en el comedor a las doce treinta.

—Ya no importan Kaelen ni Reyes —respondió Virginia, desplegando el mapa holográfico de las profundidades del planeta—. El Proyecto Arquímedes ha detectado nuestra sincronización neural. En cuanto crucemos el umbral de las ruinas prohibidas, la Academia entera entrará en estado de excepción. Ya no seremos cadetes disidentes; seremos la anomalía ontológica más peligrosa del Imperio.

Oscar asintió. Miró la inscripción grabada en el umbral de titanio que daba acceso al pozo de descenso: «SOLO LA CENIZA PERMANECE».

—Que vengan —dijo Oscar, encendiendo la linterna táctica y apuntando al abismo—. Tenemos un punto de apoyo. Y vamos a mover su mundo.

Fin del Libro I: La Voluntad de las Cenizas.
La historia continuará en el Libro II: El Velo de la Historia Oficial."""
        }
    ]

    export_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "exports")
    os.makedirs(export_dir, exist_ok=True)
    output_epub = os.path.join(export_dir, "Arquimedes_Libro_I_La_Voluntad_de_las_Cenizas_Completo.epub")
    
    # Rutas de portada oficial
    cover_outer = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "frontend", "assets", "portada2.jpg")
    cover_inner = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "frontend", "assets", "LaVoluntadDeLasCenizas.jpg")

    create_epub(
        passages=passages,
        output_path=output_epub,
        book_title="Arquímedes // Libro I: La Voluntad de las Cenizas",
        author="Oscar Bueno"
    )
    
    print(f"Obra completa compilada exitosamente en:\n{output_epub}")
    print(f"Tamaño del archivo: {os.path.getsize(output_epub)} bytes")
    return output_epub

if __name__ == "__main__":
    build_complete_canonical_novel()
